from discord.ext import commands

class CustomBot(commands.Bot):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_message_delete(self, message):
        channel = message.channel

        # If it's a message from bot, ignore it
        if message.author.bot:
            return

        await channel.send(f'The following message from {message.author} has been deleted!\n\n{message.content}')
