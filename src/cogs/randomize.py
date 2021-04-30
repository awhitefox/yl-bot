import re
import random
from discord.ext import commands


class Randomize(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx: commands.Context, *dice):
        response = []
        result = 0
        for d in dice:
            if not re.match('^[0-9]+d[0-9]+$', d):
                await ctx.send(f'Не удалось распознать куб {d}')
                return
            count, faces = map(int, d.split('d', 1))
            values = [random.randint(1, faces) for _ in range(count)]
            response.append(' + '.join(map(str, values)))
            result += sum(values)
        if len(response) == 0:
            response = '0'
        elif len(response) == 1:
            response = response[0]
        else:
            response = ' + '.join(map(lambda x: f'({x})', response))
        response += f' = {result}'
        await ctx.send(response)

    @commands.command(name='8ball')
    async def eight_ball(self, ctx: commands.Context, *, question: str):
        answers = [
            'Бесспорно',
            'Предрешено ',
            'Никаких сомнений',
            'Определённо да',
            'Можешь быть уверен в этом',

            'Мне кажется — «да»',
            'Вероятнее всего',
            'Хорошие перспективы',
            'Знаки говорят — «да»',
            'Да',

            'Пока не ясно, попробуй снова',
            'Спроси позже',
            'Лучше не рассказывать',
            'Сейчас нельзя предсказать',
            'Сконцентрируйся и спроси опять',

            'Даже не думай',
            'Мой ответ — «нет»',
            'По моим данным — «нет»',
            'Перспективы не очень хорошие',
            'Весьма сомнительно'
        ]
        await ctx.send(random.choice(answers))

    @commands.command()
    async def probability(self, ctx: commands.Context, *, question: str):
        await ctx.send(f'Вероятность этого: {random.randint(1, 99)}%')

    @commands.command()
    async def randint(self, ctx: commands.Context, bottom: int, top: int):
        await ctx.send(str(random.randint(bottom, top)))


def setup(bot: commands.Bot):
    bot.add_cog(Randomize(bot))
