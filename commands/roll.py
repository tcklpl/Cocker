from discord.ext import commands
from discord.ext.commands.cog import Cog
from utils import input_utils

class Roll(Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name = 'roll', aliases = ['r'])
    async def roll(self, ctx):

        if (input_utils.check_if_will_execute()):
            await ctx.channel.send(ctx.author.mention + " Vai se foder")
            return

        try:
            dices, simple_values = input_utils.split_raw_input_into_dices(ctx.message.content)
            final = self.roll_and_join_dices_and_numbers(dices, simple_values)

            if len(final) >= 2000:
                raise ValueError("A resposta tem mais de 2k caracteres, oq caralhos tu ta tentando rolar?")

            await ctx.channel.send(ctx.author.mention + " " + final)
        except (ValueError, AttributeError) as e:
            await ctx.channel.send(ctx.author.mention + " **Erro ao executar o comando:** " + str(e))

    def roll_and_join_dices_and_numbers(self, dice_arr, simple_numbers):

        final_str = ''
        final_str_parts = []
        total = 0

        for dice in dice_arr:
            subtotal, substr = dice.roll()
            total += subtotal
            final_str_parts.append(substr)
        
        for num in simple_numbers:
            total += num
            final_str_parts.append(str(num))

        for i in range(len(final_str_parts)):
            final_str += final_str_parts[i].replace('-', '') if i > 0 else final_str_parts[i]
            final_str += " = " if i == (len(final_str_parts) - 1) else " + " if '-' not in final_str_parts[i + 1] else " - "
        
        final_str += str(total)

        return final_str

def setup(bot):
    bot.add_cog(Roll(bot))