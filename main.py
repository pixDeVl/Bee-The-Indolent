import discord
from discord.ext.commands import Bot, when_mentioned
import logging
from os import getenv, listdir
import dotenv
import datetime
import logging

log = logging.getLogger('discord')
class BeeBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        discord.utils.setup_logging(level=logging.DEBUG)
        self.start_time = datetime.datetime.now()
        self.log = log
    async def setup_hook(self):
        for filename in listdir("./cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()
        log.info('Loaded Cogs')
    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Game(name='being eepy'))
        
        





intents = discord.Intents.all()
bot = BeeBot(when_mentioned,intents=intents)



def main():
    
    dotenv.load_dotenv('.env')
    bot.run(getenv('BOT_TOKEN'))


if __name__ == "__main__":
    main()