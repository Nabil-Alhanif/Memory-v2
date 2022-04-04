import discord
import os

from dotenv import load_dotenv

from bot import CustomBot

from cogs.greetings import Greetings
from cogs.random.randomizer import Randomizer
from cogs.scraper.savemyexams import SaveMyExams
from cogs.translate import Translate
from cogs.commandErrHandler import CommandErrHandler

def main():
    TOKEN = os.getenv('TOKEN')

    intents = discord.Intents.default()
    intents.members = True

    bot = CustomBot(
        command_prefix='$',
        intents=intents,
        case_insensitive=True
    )

    bot.add_cog(Greetings(bot))
    bot.add_cog(Randomizer(bot))
    bot.add_cog(SaveMyExams(bot))
    bot.add_cog(Translate(bot))
    bot.add_cog(CommandErrHandler(bot))

    bot.run(TOKEN)

if __name__ == "__main__":
    load_dotenv()
    main()
