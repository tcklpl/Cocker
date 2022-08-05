from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands import Context
from utils import input_utils

class Boundaries(Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name = 'boundaries', aliases = ['b'])
    async def boundaries(self, ctx: Context):

        if (input_utils.check_if_will_execute()):
            await ctx.channel.send(ctx.author.mention + " Vai se foder")
            return

        try:
            dices, simple_values = input_utils.split_input_into_dices(''.join(ctx.message.content.split()[1:]))
            min, max = self.get_roll_boundaries(dices, simple_values)

            await ctx.channel.send(ctx.author.mention + " Você pode rolar isso entre {} e {}".format(str(min), str(max)))
        except (ValueError, AttributeError) as e:
            await ctx.channel.send(ctx.author.mention + " **Erro ao executar o comando:** " + str(e))

    def get_roll_boundaries(self, dice_arr, simple_numbers):
        min = 0
        max = 0
        for dice in dice_arr:
            dice_min, dice_max = dice.boundaries()
            min += dice_min
            max += dice_max

        for number in simple_numbers:
            min += number
            max += number
        
        return min, max

def setup(bot):
    bot.add_cog(Boundaries(bot))