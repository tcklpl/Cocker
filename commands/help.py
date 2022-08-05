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
        
        help = '```\
        Comandos Básicos:\n\
            .r <dados> : rola os dados\n\
            .b <dados> : mostra o mínimo e máximo que é possível tirar com os dados informados.\n\
            .h         : mostra essa mensagem.\n\
            .pd        : roda os dados para criação de personagem.\n\
        Batalhas:\n\
            .bc <NOME> : cria uma batalha com o nome desejado.\n\
            .bj <NOME BATALHA> <NOME JOGADOR> <OPCIONAL: DADO DE INICIATIVA> : entra na batalha desejada com ou sem um dado de iniciativa (por padrão será um d20).\n\
            .bk <NOME BATALHA> <NOME JOGADOR> : remove o jogador da batalha.\n\
            .bs <NOME BATALHA> : mostra a ordem de iniciativa da batalha.\n\
            .br <NOME BATALHA> : remove a batalha.\n\
            .bl : lista as batalhas atuais no canal.\
        ```'

        await ctx.channel.send(ctx.author.mention + " " + help)

def setup(bot):
    bot.add_cog(Help(bot))