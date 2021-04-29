import os
import requests
import datetime as dt
import discord
from discord.ext import commands
from typing import Dict, Any, Optional


class Weather(commands.Cog):
    api_url = 'https://api.openweathermap.org/data/2.5'
    api_key = os.environ['OPENWEATHER_KEY']

    lang = 'ru'
    units = 'metric'

    city_not_found_embed = discord.Embed(title='Город не найден',
                                         description='Проверьте правильность введенного названия')

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx: commands.Context, *, city: str):
        w = self._get_current_weather(city)
        if w:
            weather_emoji = self._get_emoji_by_condition_code(w['weather'][0]['id'])
            weather_desc = w['weather'][0]['description'].capitalize()

            temp = round(w['main']['temp'], 1)
            pressure = round(w['main']['pressure'] / 1.333, 1)
            humidity = w['main']['humidity']

            wind_speed = w['wind']['speed']
            wind_compass = self._degrees_to_compass(w['wind']['deg'])

            lines = [
                f'{weather_emoji} **{weather_desc}**',
                f'',
                f'**Температура:** {temp} °C',
                f'**Атмосферное давление:** {pressure} мм рт. ст.',
                f'',
                f'**Влажность воздуха:** {humidity}%',
                f'**Ветер:** {wind_speed} м/c {wind_compass}'
            ]
            embed = discord.Embed(title='Погода в городе ' + w['name'], description='\n'.join(lines))
        else:
            embed = self.city_not_found_embed
        await ctx.send(embed=embed)

    @commands.command()
    async def forecast(self, ctx: commands.Context, *, city: str):
        current = self._get_current_weather(city)

        daily = None
        if current:
            daily = self._get_weather_forecast(current['coord']['lat'], current['coord']['lon'])

        if daily:
            embed = discord.Embed(title='Прогноз погоды в городе ' + current['name'])

            for d in daily['daily']:
                weather_emoji = self._get_emoji_by_condition_code(d['weather'][0]['id'])
                weather_desc = d['weather'][0]['description'].capitalize()

                temp_min = round(d['temp']['min'], 1)
                temp_max = round(d['temp']['max'], 1)

                wind_speed = d['wind_speed']
                wind_compass = self._degrees_to_compass(d['wind_deg'])

                rain = d.get('rain')

                s = f'{weather_emoji} **{weather_desc}**\n'
                lines = [
                    f':thermometer: От {temp_min} до {temp_max} °C',
                    f':dash: {wind_speed} м/c {wind_compass}'
                ]
                if rain:
                    lines.append(f':umbrella: {rain} мм')

                date = dt.datetime.utcfromtimestamp(d['dt']).strftime('%d.%m')

                embed.add_field(name=date, value=s + (' \u200b' * 5).join(lines) + '\n\u200b', inline=False)
        else:
            embed = self.city_not_found_embed
        await ctx.send(embed=embed)

    def _get_current_weather(self, city: str) -> Optional[Dict[str, Any]]:
        url = self.api_url + '/weather'
        params = {
            'appid': self.api_key,
            'q': city,
            'units': self.units,
            'lang': self.lang
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    def _get_weather_forecast(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        url = self.api_url + '/onecall'
        params = {
            'appid': self.api_key,
            'lat': lat,
            'lon': lon,
            'units': self.units,
            'lang': self.lang
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def _degrees_to_compass(d: float) -> str:
        dirs = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
        step = 360 / len(dirs)
        return dirs[round((d + step) % 360 / step) - 1]

    @staticmethod
    def _get_emoji_by_condition_code(code: int) -> str:
        m = code // 100
        if m == 8:
            return {
                800: ':sunny:',
                801: ':white_sun_small_cloud:',
                802: ':white_sun_cloud:',
                803: ':cloud:',
                804: ':cloud:'
            }[code]
        else:
            return {
                2: ':thunder_cloud_rain:',
                3: ':white_sun_rain_cloud:',
                5: ':cloud_rain:',
                6: ':cloud_snow:',
                7: ':fog:',
            }[m]


def setup(bot: commands.Bot):
    bot.add_cog(Weather(bot))
