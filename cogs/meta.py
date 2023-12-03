import discord
from discord.ext import commands

class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.log = bot.log
        
    @discord.app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        """Sents a Pong! back to the caller with the current latency

        Args:
            interaction (discord.Interaction): The interaction from the app commands
        """
        await interaction.response.send_message(f'Pong! `{str(round(self.bot.latency * 1000))}` ms')
        
    
    
    
    
    
async def setup(bot):
    await bot.add_cog(Meta(bot))
    bot.log.info('Loaded Meta')