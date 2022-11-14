from discord.ext import commands
import discord

import traceback
import sys
from datetime import datetime

from cogs.utils import embed_templates
from cogs.utils.misc_utils import ignore_exception


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """
        Prints command execution metadata
        """

        self.bot.logger.info(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ' +
            f'{"❌ " if ctx.command_failed else "✔ "} {ctx.command} - ' +
            f'{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) | ' +
            f'{ctx.guild.id}-{ctx.channel.id}-{ctx.message.id}'
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Returns something based on the type of command error
        """

        # Reset cooldown if command throws an error
        with ignore_exception(AttributeError):
            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)

        # Ignore command's own error handling
        if hasattr(ctx.command, 'on_error'):
            return

        # Ignored errors
        ignored = commands.CommandNotFound
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        send_help = (
            commands.MissingRequiredArgument,
            commands.TooManyArguments,
            commands.BadArgument
        )
        if isinstance(error, send_help):
            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)
            return await ctx.send_help(ctx.command)

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = ', '.join(error.missing_perms)
            embed = embed_templates.error_warning(ctx, text='Jeg mangler følgende tillatelser:\n\n' +
                                                            f'```\n{permissions}\n```')
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            permissions = ', '.join(error.missing_perms)
            embed = embed_templates.error_warning(ctx, text='Du mangler følgende tillatelser\n\n' +
                                                            f'```\n{permissions}\n```')
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = embed_templates.error_fatal(ctx, text='Bare boteieren kan gjøre dette')
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = embed_templates.error_warning(ctx, text='Kommandoen har nettopp blitt brukt' +
                                                            f'Prøv igjen om `{error.retry_after:.1f}` sekunder.')
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = embed_templates.error_fatal(ctx, text='Denne kommandoen kan bare utføres i servere')
                return await ctx.send(embed=embed)
            except discord.errors.Forbidden:  # Thrown if bot is blocked by the user or if the user has closed their DMs
                print("DM Blocked!")

        elif isinstance(error, commands.DisabledCommand):
            pass

        elif isinstance(error, commands.CheckFailure):
            return

        embed = embed_templates.error_fatal(ctx, text='En ukjent feil oppstod!')
        await ctx.send(embed=embed)

        # Log full exception to file
        self.bot.logger.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))


async def setup(bot):
    await bot.add_cog(Errors(bot))
