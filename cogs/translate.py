import goslate

from discord.ext import commands

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = goslate.Goslate()
        self.roman_gs = goslate.Goslate(writing=goslate.WRITING_ROMAN)

    @commands.command(name='trans', help="Translate text into English")
    async def trans(self, ctx, *args):
        query = str(" ".join(args)).strip()
        res = self.gs.translate(query, 'en')

        await ctx.send(res)

    @commands.command(name='detect', help="Detect the language of the text")
    async def detect(self, ctx, *args):
        query = str(" ".join(args)).strip()
        id = self.gs.detect(query)
        res = self.gs.get_languages()[id]

        await ctx.send(res)
