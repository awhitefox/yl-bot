import pytz
import datetime as dt
import discord
from discord.ext import commands
from typing import Optional
from table import Table
TIMEZONE = pytz.timezone('Europe/Moscow')
WEEKDAYS = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday'
]


class SchoolTimetables(commands.Cog):
    db_table_name = 'school_timetables'

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def timetable(self, ctx: commands.Context):
        return

    @timetable.command()
    async def create(self, ctx: commands.Context, cl: str, tag: Optional[str] = None):
        table = Table(self.db_table_name)
        table.insert({
            'guild_id': ctx.guild.id,
            'class': cl,
            'tag': tag
        })
        await ctx.send('Расписание создано')

    @timetable.command()
    async def add_lesson(self, ctx: commands.Context, cl: str, weekday: int, start: str, end: str,
                         title: str, room: str, teacher: str, tag: Optional[str] = None):
        table = Table(self.db_table_name)
        table.where(f'guild_id={ctx.guild.id}')
        table.where(f'class=\'{cl}\'')
        if tag:
            table.where(f'tag=\'{tag}\'')

        start = self.parse_time(start)
        end = self.parse_time(end)

        current = table.get_selected_data()[0][WEEKDAYS[weekday]]
        new = ':'.join(map(str, (start, end, title, room, teacher)))
        if current:
            new = ';' + current

        table.update(**{
            WEEKDAYS[weekday]: new
        })
        await ctx.send('Готово!')

    @timetable.command()
    async def for_class(self, ctx: commands.Context, cl: str, tag: Optional[str] = None):
        table = Table(self.db_table_name)

        table.where(f'guild_id={ctx.guild.id}')
        table.where(f'class=\'{cl}\'')
        if tag:
            table.where(f'tag=\'{tag}\'')
        data = table.get_selected_data()

        if len(data) > 0:
            data = data[0]
            now = dt.datetime.now(TIMEZONE)
            if now.weekday() == 6:
                embed = discord.Embed(title='Сегодня воскресенье', description='Можете отдыхать')
            else:
                embed = discord.Embed(title='Ваше распирание', description='')
                time_now = now.timestamp() / 60

                lessons = data[WEEKDAYS[now.weekday()]].split(';')
                if len(lessons) > 0:
                    for lesson in lessons:
                        start, end, title, room, teacher = lesson.split(':')
                        text = f'{start // 60}{start % 60}:{end // 60}{end % 60} {title}, каб. ' \
                               f'{room}, {teacher}'
                        if start < time_now < end:
                            text = '**' + text + '**'
                        embed.description += text + '\n'
                else:
                    embed.description = 'Нет занятий'
        else:
            embed = discord.Embed(title='Ничего не найдено',
                                  description='Проверьте правильность введенных данных')
        await ctx.send(embed=embed)

    @staticmethod
    def parse_time(s: str) -> int:
        m, s = map(int, s.split(':'))
        return m * 60 + s


def setup(bot: commands.Bot):
    bot.add_cog(SchoolTimetables(bot))
