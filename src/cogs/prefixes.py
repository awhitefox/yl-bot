import os
import discord
from discord.ext import commands
from table import Table


class Prefixes(commands.Cog):
    db_table_name = 'prefixes'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='get_prefix')
    async def get_prefix_command(self, ctx: commands.Context):
        await ctx.send(self.get_prefix(ctx.guild.id))

    @commands.command(name='set_prefix')
    @commands.has_permissions(manage_guild=True)
    async def set_prefix_command(self, ctx: commands.Context, prefix: str):
        self.set_prefix(ctx.guild.id, prefix)
        await ctx.send(f'Префикс для команд изменен на {prefix}')

    @classmethod
    def get_prefix(cls, guild_id: int) -> str:
        table = Table(cls.db_table_name)
        table.where(f'guild_id={guild_id}')
        data = table.get_selected_data()

        if data:
            prefix = data[0]['prefix']
            return prefix
        else:
            return os.environ['PREFIX']

    @classmethod
    def set_prefix(cls, guild_id: int, prefix: str) -> None:
        table = Table(cls.db_table_name)
        table.where(f'guild_id={guild_id}')
        data = table.get_selected_data()
        if data:
            table.update(prefix=prefix)
        else:
            table.insert({'guild_id': guild_id, 'prefix': prefix})


def resolve_prefix(bot: commands.Bot, message: discord.Message):
    return Prefixes.get_prefix(message.guild.id)


def setup(bot: commands.Bot):
    bot.add_cog(Prefixes(bot))
