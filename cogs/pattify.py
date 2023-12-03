import discord
from discord.ext import commands
from discord import app_commands
import sys
sys.path.append('../utils')
from utils.patpat_creator import PatPatCreator
import regex
from typing import Union

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
        
        self.pattify_user = app_commands.ContextMenu(name='Pattify', callback=self.pattify_user)
        self.bot.tree.add_command(self.pattify_user)

    async def pattify_msg(self, interaction: discord.Interaction, message: discord.Message):
        """Message Context Menu to make a patting gif from all image links and attachments in the message

        Args:
            interaction (discord.Interaction): The context menu interaction
            message (discord.Message): The message the command is preformed on
        """
        await interaction.response.defer()
        urls = regex.findall(image_match, message.content)
        self.log.debug(urls)
        buffer = []
        for i in urls:
            gif = await PatPatCreator(image_url=i).create_gif()
            buffer.append(gif)
        self.log.debug(buffer)
        files = [discord.File(i, "pat.gif") for i in buffer]
        self.log.debug('Files: ' + str(files))
        await interaction.followup.send(files=files)
        
    async def pattify_user(self, interaction: discord.Interaction, user: Union[discord.Member, discord.User]):
        """User Context Menu to make a pat gif from avatar

        Args:
            interaction (discord.Interaction): Context Menu Interaction
            user (Union[discord.Member, discord.User]): The user the command is used on
        """
        await interaction.response.defer()
        url = user.display_avatar.url
        gif = await PatPatCreator(image_url=url).create_gif()
        await interaction.followup.send(file=discord.File(gif, 'pat.gif'))
async def setup(bot):
    await bot.add_cog(Pattify(bot))
    bot.log.info('Loaded Pattify')