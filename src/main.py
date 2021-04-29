import os
import discord
from discord.ext import commands
import db_funcs

if os.path.isfile('../.env'):
    from dotenv import load_dotenv
    load_dotenv(encoding='utf8')

bot = commands.Bot(os.environ['PREFIX'], help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    embed = discord.Embed(title=':x: Не удалось выполнить команду', description=str(error))
    await ctx.send(embed=embed)


@bot.command(name='help')
async def help_command(ctx: commands.Context):
    embed = discord.Embed(title='Помощь по командам', description=os.environ['HELP'])
    await ctx.send(embed=embed)
  

db_funcs.set_connection(os.environ['DATABASE_URL'])
bot.load_extension('cogs.cats')
bot.load_extension('cogs.weather')
bot.run(os.environ['TOKEN'])
