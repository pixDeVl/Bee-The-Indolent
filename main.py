import discord
from discord.ext.commands import Bot, when_mentioned_or
import logging
from os import getenv, listdir
import dotenv
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


class BeeBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = datetime.datetime.now()
        self.log = logging.getLogger('discord')
        rotatingHandler = TimedRotatingFileHandler(filename='bee_bot.log', when='midnight', backupCount=14)
        rotatingHandler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(rotatingHandler)
    async def setup_hook(self):
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await self.load_extension(f"cogs.{filename[:-3]}")
        self.log.info('Loaded Cogs')
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game(name='being eepy'))
        
        





intents = discord.Intents.all()
bot = BeeBot(when_mentioned_or('*'),intents=intents)



def main():
    dotenv.load_dotenv('.env')
    bot.run(getenv('BOT_TOKEN'),log_level=logging.INFO)


if __name__ == "__main__":
    main()