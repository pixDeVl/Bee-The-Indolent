import discord
from discord.ext import commands
from datetime import datetime

class Meta(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.log = bot.log
        self.tree = bot.tree
    @discord.app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        """Sents a Pong! back to the caller with the current latency

        Args:
            interaction (discord.Interaction): The interaction from the app commands
        """
        await interaction.response.send_message(f'**Pong!** `{str(round(self.bot.latency * 1000))}` ms\n **Current Uptime:** `{str(datetime.now()-self.bot.start_time)}`')
        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx, guild: int = None):
        """Manually syncs the command tree [Owner Only]
        
        Args:
            ctx: The context of the message command
            guild (Optional[int]): The id of the guild to sync the command tree for(if given as 0, use current)
        """
        if guild == 0: guild = ctx.guild.id
        if guild:
            self.log.info(f'Command tree syncing for guild {guild}')
            await self.tree.sync(guild=discord.Object(guild))
            self.log.info(f'Command tree synced for guild {guild}')
            await ctx.send(f"Command tree synced successfully for guild {guild}!")
        else:
            self.log.info('Command tree syncing globally')
            await self.tree.sync()
            self.log.info('Command tree synced')
            await ctx.send("Command tree synced successfully!")
    
    
    
    
    
async def setup(bot):
    await bot.add_cog(Meta(bot))
    bot.log.info('Loaded Meta')