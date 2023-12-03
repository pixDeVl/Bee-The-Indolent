import discord
from discord.ext import commands
from discord import app_commands
import sys
sys.path.append('../utils')
from utils.patpat_creator import PatPatCreator
import regex

image_match = r'(https?:\/\/\S*\.(?:png|jpg))'

class Pattify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log 
        self.pattify_menu = app_commands.ContextMenu(
            name='Pattify',
            callback=self.pattify_msg,
        )
        self.bot.tree.add_command(self.pattify_menu)
        
        

    async def pattify_msg(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        urls = regex.findall(image_match, message.content)
        print(urls)
        buffer = []
        for i in urls:
            gif = await PatPatCreator(image_url=i).create_gif()
            buffer.append(gif)
        # discord.File(patpat_buffer, filename='patpat.gif')
        print(buffer)
        files = [discord.File(i, "pat.gif") for i in buffer]
        print('Files: ' + str(files))
        await interaction.followup.send(files=files)
async def setup(bot):
    await bot.add_cog(Pattify(bot))
    bot.log.info('Loaded Pattify')