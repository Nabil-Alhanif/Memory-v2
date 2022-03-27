import discord
import os

from bot import CustomBot

from cogs.commandErrHandler import CommandErrHandler

def main():
    TOKEN = os.environ['TOKEN']

    intents = discord.Intents.default()
    intents.members = True

    bot = CustomBot(
        command_prefix='$',
        intents=intents,
        case_insensitive=True
    )

    bot.add_cog(CommandErrHandler(bot))

    bot.run(TOKEN)

if __name__ == "__main__":
    main()
