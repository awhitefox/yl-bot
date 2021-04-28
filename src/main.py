import os
from discord.ext import commands
if os.path.isfile('../.env'):
    from dotenv import load_dotenv
    load_dotenv(encoding='utf8')

bot = commands.Bot(os.environ['PREFIX'])


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f':x: **Не удалось выполнить команду:** {error}')


bot.run(os.environ['TOKEN'])
