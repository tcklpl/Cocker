from typing import final
from discord.ext import commands
from discord.ext.commands.cog import Cog
from utils import input_utils
from utils.dice_utils import roll_and_join_dices_and_numbers

class Roll(Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name = 'roll', aliases = ['r'])
    async def roll(self, ctx):

        if (input_utils.check_if_will_execute()):
            await ctx.channel.send(ctx.author.mention + " Vai se foder")
            return

        try:
            dices, simple_values = input_utils.split_input_into_dices(''.join(ctx.message.content.split()[1:]))
            total, final = roll_and_join_dices_and_numbers(dices, simple_values)

            if len(final) >= 2000:
                raise ValueError("A resposta tem mais de 2k caracteres, oq caralhos tu ta tentando rolar?")

            await ctx.channel.send(ctx.author.mention + " " + final)
        except (ValueError, AttributeError) as e:
            await ctx.channel.send(ctx.author.mention + " **Erro ao executar o comando:** " + str(e))

def setup(bot):
    bot.add_cog(Roll(bot))