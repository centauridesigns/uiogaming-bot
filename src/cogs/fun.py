from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def norskeuniversiteter(self, ctx: commands.Context):
        await ctx.send('<https://imgur.com/a/uGopaSq>')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ifi(self, ctx: commands.Context):
        await ctx.send('https://i.imgur.com/ypyK1mi.jpg')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ifi2(self, ctx: commands.Context):
        await ctx.send('https://i.imgur.com/ZqgZEEA.jpg')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ifi3(self, ctx: commands.Context):
        await ctx.send('https://i.imgur.com/Gx9DQE5.jpg')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def uio(self, ctx: commands.Context):
        await ctx.send('https://i.imgur.com/188MoIV.jpg')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ntnu(self, ctx: commands.Context):
        await ctx.send('https://twitter.com/NTNU/status/970667413564993536')

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ntnu2(self, ctx: commands.Context):
        await ctx.send('https://i.imgur.com/h84fknj.jpg')


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
