import os
import requests
import discord
from discord.ext import commands


class Weather(commands.Cog):
    api_url = 'https://api.openweathermap.org/data/2.5/onecall'
    api_key = os.environ['OPENWEATHER_KEY']
    default_city = 'Moscow'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def weather(self, ctx: commands.Context):
        if ctx.invoked_subcommand is not None:
            return
        pass

    @weather.command()
    async def forecast(self, ctx: commands.Context):
        pass

    def get_forecast(self, city):
        pass

    @staticmethod
    def get_emoji_by_condition_code(code):
        return {
            2: ':thunder_cloud_rain:',
            3: ':white_sun_rain_cloud:',
            5: ':cloud_rain:',
            6: ':cloud_snow:',
            7: ':fog:',
            8: {
                800: ':sunny:',
                801: ':white_sun_small_cloud:',
                802: ':white_sun_cloud:',
                804: ':cloud:'
            }[code]
        }[code % 100]


def setup(bot: commands.Bot):
    bot.add_cog(Weather(bot))
