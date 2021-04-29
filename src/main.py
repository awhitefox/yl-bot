import os
import discord
from discord.ext import commands
if os.path.isfile('../.env'):
    from dotenv import load_dotenv
    load_dotenv(encoding='utf8')

bot = commands.Bot(os.environ['PREFIX'], help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f':x: **Не удалось выполнить команду:** {error}')


@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="Помощь по командам", description=os.environ['HELP'])
    await ctx.send(embed=embed)


bot.run(os.environ['TOKEN'])
