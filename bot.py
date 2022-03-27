from discord.ext import commands

class CustomBot(commands.Bot):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        await self.process_commands(message)
