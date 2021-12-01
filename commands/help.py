from discord.ext import commands
from discord.ext.commands.cog import Cog
from utils import input_utils

class Help(Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name = 'commands', aliases = ['h'])
    async def help(self, ctx):

        if (input_utils.check_if_will_execute()):
            await ctx.channel.send(ctx.author.mention + " Vai se foder")
            return
        
        help = 'Comandos:\n```\
            .r <dados> : rola os dados\n\
            .b <dados> : mostra o mínimo e máximo que é possível tirar com os dados informados.\n\
            .h         : mostra essa mensagem.\n\
            .pd        : roda os dados para criação de personagem.\
        ```'

        await ctx.channel.send(ctx.author.mention + " " + help)

def setup(bot):
    bot.add_cog(Help(bot))