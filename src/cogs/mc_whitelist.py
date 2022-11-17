import discord
from discord import app_commands
from discord.ext import commands
from mcrcon import MCRcon
import requests

from cogs.utils import embed_templates


class MCWhitelist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cursor = self.bot.db_connection.cursor()
        self.init_db()

    def init_db(self):
        """Create the necessary tables for the mc_whitelist cog to work."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mc_whitelist (
                discord_id BIGINT PRIMARY KEY,
                minecraft_id TEXT NOT NULL
            );
            """
        )
        self.bot.db_connection.commit()

    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.checks.cooldown(1, 5)
    @app_commands.command()
    async def whitelist(self, interaction: discord.Interaction, minecraftbrukernavn: str):
        """Whitelist Minecraftbrukeren din på serveren vår"""

        # Fetch minecraft uuid from api
        data = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{minecraftbrukernavn}", timeout=10).json()
        if data.status_code != 200:
            return await interaction.response.send_message(
                embed=embed_templates.error_fatal(interaction, text=f"Brukeren `{minecraftbrukernavn}` finnes ikke på minecraft"),
                ephemeral=True
            )

        data = data.json()

        # check if the discord user or minecraft user is in the db
        self.cursor.execute(
            """
            SELECT *
            FROM mc_whitelist
            WHERE minecraft_id = %s OR discord_id = %s
            """, (data["id"], interaction.user.id)
        )
        if self.cursor.fetchone():
            return await interaction.response.send_message(
                embed=embed_templates.error_fatal(
                    interaction,
                    text="Du har allerede whitelisted en bruker eller så er brukeren du oppga whitelisted"
                )
            )

        # Whitelist user on minecraft server
        # Unfortunately, this requires an active connection to the server, with correct credentials
        with MCRcon(host="127.0.0.1", password=self.bot.mc_rcon_password, port=25575) as mcr:
            mcr.command(f"whitelist add {data['name']}")
            mcr.command("whitelist reload")

        # Add user to db
        self.cursor.execute(
            """
            INSERT INTO mc_whitelist (discord_id, minecraft_id)
            VALUES (%s, %s)
            """,
            (interaction.user.id, data["id"]),
        )
        self.bot.db_connection.commit()

        await interaction.response.send_message(
            embed=embed_templates.success(
                interaction, text=f"`{data['name']}` er nå tilknyttet din discordbruker og whitelisted!"
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(MCWhitelist(bot))
