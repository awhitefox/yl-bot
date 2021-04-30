import requests
from discord.ext import commands
from typing import Optional


class Cats(commands.Cog):
    api_url = 'https://api.thecatapi.com/v1'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context, breed: Optional[str] = None):
        if breed is None:
            await ctx.send(self._get_random_cat_url())
        else:
            breed_id = self._find_breed_id(breed)
            if breed_id:
                await ctx.send(self._get_cat_url_by_breed_id(breed_id))
            else:
                await ctx.send('Ничего не найдено')

    def _get_random_cat_url(self) -> str:
        data = requests.get(self.api_url + '/images/search').json()
        return data[0]['url']

    def _get_cat_url_by_breed_id(self, breed_id: str) -> str:
        data = requests.get(self.api_url + '/images/search', params={'breed_id': breed_id}).json()
        return data[0]['url']

    def _find_breed_id(self, query: str) -> Optional[str]:
        data = requests.get(self.api_url + '/breeds/search', params={'q': query}).json()
        return data[0]['id'] if len(data) > 0 else None


def setup(bot: commands.Bot):
    bot.add_cog(Cats(bot))
