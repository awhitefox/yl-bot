import requests
from discord.ext import commands


class Cats(commands.Cog):
    api_url = 'https://api.thecatapi.com/v1/images/search'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx: commands.Context):
        await ctx.send(self.get_random_cat_url())

    def get_random_cat_url(self) -> str:
        return requests.get(self.api_url).json()[0]['url']


def setup(bot: commands.Bot):
    bot.add_cog(Cats(bot))
