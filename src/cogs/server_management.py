import discord
from discord.ext import commands
from typing import Optional


class ServerManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None, limit: int = 200):
        if channel is None:
            channel = ctx.channel
        if channel.permissions_for(ctx.author).manage_messages:
            deleted = await channel.purge(limit=limit)
            await ctx.send(f'Удалено сообщений: {len(deleted)}')
        else:
            await ctx.send(f'У вас недостаточно прав, чтобы удалять сообщения в этом канале')

    @commands.command()
    @commands.guild_only()
    async def delete_channels(self, ctx: commands.Context, channels: commands.Greedy[discord.TextChannel]):
        i = 0
        for ch in channels:
            if ch.permissions_for(ctx.author).manage_channels:
                if not ch.permissions_for(ctx.guild.me).manage_channels:
                    await ctx.send(f'У меня недостаточно прав, чтобы удалить канал {ch.mention}')
                if ch == ctx.channel:
                    await ctx.send(f'Этой командой нельзя удалить текущий канал!')
                else:
                    await ch.delete()
                    i += 1
            else:
                await ctx.send(f'У вас недостаточно прав, чтобы удалить канал {ch.mention}')
        await ctx.send(f'Удалено каналов: {i}')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def delete_roles(self, ctx: commands.Context, roles: commands.Greedy[discord.Role]):
        i = 0
        bot_top_role = ctx.guild.me.top_role
        for r in roles:
            if ctx.author.top_role <= r and ctx.author.id != ctx.guild.owner_id:
                await ctx.send(f'У вас недостаточно прав, чтобы удалить роль {r.name}')
            elif bot_top_role <= r:
                await ctx.send(f'У меня недостаточно прав, чтобы удалить роль {r.name}')
            else:
                await r.delete()
                i += 1
        await ctx.send(f'Удалено ролей: {i}')


def setup(bot: commands.Bot):
    bot.add_cog(ServerManagement(bot))
