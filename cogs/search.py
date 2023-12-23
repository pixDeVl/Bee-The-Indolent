import discord
from discord.ext import commands
from discord import app_commands
import requests
from typing import List

embed_color = 0x34e5eb

class Search(commands.GroupCog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.log = bot.log

    

    
    
    @app_commands.command(name='wikipedia')
    async def wikipedia_search(self, interaction: discord.Interaction, query: str):
        """Searches Wikipedia"""
        # Add your Wikipedia search logic here
        results = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'opensearch',
                'format': 'json',
                'limit': 25,
                'namespace': 0,
                'search': query
            }
        ).json()
        embed = discord.Embed(color=embed_color, title=f'Wikipedia Search Results for {query}', description='Here are the results from your search')
        if len(results[1]) < 1: embed = discord.Embed(color=embed_color, title='Womp Womp', description='No Results found for that search.')
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        for index, result in enumerate(results[1]):
            embed.add_field(name="", value=f'[{result}]({results[3][index]})', inline=False)
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name='define')
    async def define(self, interaction: discord.Interaction, word: str):
        """Defines a word"""
        request = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}').json()
        mean_embed_list = []
        try:
            for mean in request[0]['meanings']:
                mean_embed = discord.Embed(color=embed_color, title=mean['partOfSpeech'])
                for defs in mean['definitions']:
                    value = defs.get('example', '')
                    if value != '': value = f'Example: `{value}`'
                    mean_embed.add_field(name=defs['definition'], value=value, inline=False)
                mean_embed_list.append(mean_embed)
            msg_text = f'Showing definitions for "{request[0]["word"]}" `{request[0]["phonetic"]}`'
            await interaction.response.send_message(msg_text, embeds=mean_embed_list)
        except: KeyError
        await interaction.response.send_message(r'¯\_(ツ)_/¯ No results could be found for "{}"'.format(word), ephemeral=True)

        
        
        
        
        
    @wikipedia_search.autocomplete('query')
    async def get_wikipedia_suggestions(self, interaction: discord.Interaction, current_word: str) -> List[app_commands.Choice[str]]:
        suggestions = requests.get(
            'https://en.wikipedia.org/w/api.php',
            params={
                'action': 'opensearch',
                'format': 'json',
                'limit': 25,
                'namespace': 0,
                'search': current_word
            }
        ).json()[1]
        
        choices = [app_commands.Choice(name=suggestion, value=suggestion) for suggestion in suggestions]
        return choices[:25]

    @define.autocomplete('word')
    async def get_datamuse_suggestions(self, interaction: discord.Interaction, current_word: str) -> List[app_commands.Choice[str]]:
        suggestions = requests.get(
            'https://api.datamuse.com/sug',
            params={
                's': current_word
            }
        ).json()
        
        choices = [app_commands.Choice(name=suggestion['word'], value=suggestion['word']) for suggestion in suggestions]
        return choices[:25]

async def setup(bot):
    await bot.add_cog(Search(bot))
    bot.log.info('Loaded Search')


