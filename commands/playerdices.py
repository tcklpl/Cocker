from discord.ext import commands
from discord.ext.commands.cog import Cog
from dice import Dice
from utils import input_utils

class PlayerDices(Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name = 'playerdices', aliases = ['pd'])
    async def playerdices(self, ctx):

        if (input_utils.check_if_will_execute()):
            await ctx.channel.send(ctx.author.mention + " Vai se foder")
            return

        dices = [Dice(4, 6, False) for i in range(6)]

        total = 0
        text = "\n"
        for dice in dices:
            i_total, i_text = dice.get_as_character_dices()
            total += i_total
            text += i_text + " = " + str(i_total) + "\n"
        
        await ctx.channel.send(ctx.author.mention + " " + text)
    
def setup(bot):
    bot.add_cog(PlayerDices(bot))