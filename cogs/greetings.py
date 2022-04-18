from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hey')
    async def greet(self, ctx) -> None:
        await ctx.send(f'Hey {ctx.author.mention}')
