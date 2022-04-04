import random

from discord.ext import commands

class Randomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rgroup", help="Separate member into groups randomly")
    async def rgroup(self, ctx, group_size: int, *args) -> None:
        selection = []
        for arg in args:
            selection.append(str(arg))

        selection_length = len(selection)

        random.shuffle(selection)

        groups = []
        for i in range(0, selection_length, group_size):
            current_group = []
            for j in range(i, min(i + group_size, selection_length)):
                current_group.append(selection[j])
            groups.append(current_group)

        # Generate the result string
        res = f'Hey {ctx.author.mention}, here are the results of {selection_length} selection(s) divided into groups each with {group_size} size!'

        for i in range(0, len(groups)):
            res += f'\n\nGroup {i + 1}:'
            for sel in groups[i]:
                res += f'\n> {sel}'

        await ctx.send(res)
        return
