from twitchio.ext import commands
import os
from dotenv.main import load_dotenv
from assistant import Assistant
from play_sounds import play_text, pytts_play
from speech_files import write_file
import random

load_dotenv()
ACCESS_TOKEN = os.environ['TWITCH_TOKEN']
CHAT_TXT = "chat_says.txt"

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=['Linkeas'])
        self.Navi = Assistant()
        self.chatters_list = list()

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...

        if message.author.display_name not in self.chatters_list:
            greet = f"Saluda a ${message.author.display_name}"
            self.Navi.openai_response(main=False,chat=greet)
            self.chatters_list.append(message.author.display_name)

        if "custom-reward-id=617511c4-d233-4395-8f1f-63cae3276af4" in message.raw_data:
            print(message.content)
            print(message.author.display_name)
            write_file(CHAT_TXT, message.content)
            pytts_play(message.content)
            self.Navi.openai_response(main=False,chat=message.content)
            write_file(CHAT_TXT)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hola(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hola {ctx.author.name}!')

    @commands.command()
    async def clean(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        self.Navi.delete_text()
        await ctx.send(f'Borrando Texto...')


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
