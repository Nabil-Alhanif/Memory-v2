import random

from discord.ext import commands

class Randomizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rgs", help="Separate member into groups randomly with n size")
    async def rgs(self, ctx, group_size: int, *args) -> None:
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
        res = f'Hey {ctx.author.mention}, here are the results of {selection_length} member(s) divided into groups each with {group_size} member(s)!'

        for i in range(0, len(groups)):
            res += f'\n\nGroup {i + 1}:'
            for sel in groups[i]:
                res += f'\n> {sel}'

        await ctx.send(res)
        return

    @commands.command(name="rgg", help="Separate member into n group randomly")
    async def rgg(self, ctx, group_count: int, *args) -> None:
        selection = []
        for arg in args:
            selection.append(str(arg))

        selection_length = len(selection)

        random.shuffle(selection)

        group_size = int(selection_length / group_count)
        if selection_length % group_count != 0:
            group_size += 1

        groups = []
        for i in range(0, selection_length, group_size):
            current_group = []
            for j in range(i, min(i + group_size, selection_length)):
                current_group.append(selection[j])
            groups.append(current_group)

        # Generate the result string
        res = f'Hey {ctx.author.mention}, here are the results of {selection_length} member(s) divided into groups each with {group_size} member(s)!'

        for i in range(0, len(groups)):
            res += f'\n\nGroup {i + 1}:'
            for sel in groups[i]:
                res += f'\n> {sel}'

        await ctx.send(res)
        return
