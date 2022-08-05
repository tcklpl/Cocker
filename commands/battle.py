from ast import arg
from email.message import Message
from mimetypes import init
from re import I
from typing import Any, Dict, List
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands import Context
from dice import Dice
from utils.dice_utils import roll_and_join_dices_and_numbers
from utils.input_utils import split_input_into_dices

class BattlePlayer:

    name: str
    initiative: int
    initiative_tiebreaker: int

    def __init__(self, name, initiative) -> None:
        self.name = name
        self.initiative = initiative
        self.initiative_tiebreaker = 0

class Battle:

    name: str
    players: List[BattlePlayer]

    def __init__(self, name: str) -> None:
        self.name = name
        self.players = []
    
    def find_player(self, name: str):
        search = [x for x in self.players if x.name == name]
        return search[0] if len(search) > 0 else None

    def add_player(self, p: BattlePlayer):
        targets = list(filter(lambda x: x.initiative == p.initiative, self.players))
        if len(targets) > 0:
            # If there's only one tie
            if len(targets) == 1:
                d1 = Dice(1, 20, False)
                d2 = Dice(1, 20, False)
                v1, s1 = d1.roll()
                v2, s2 = d2.roll()
                while v1 == v2:
                    v1, s1 = d1.roll()
                    v2, s2 = d2.roll()
                targets[0].initiative_tiebreaker = v1
                p.initiative_tiebreaker = v2
            # If there's more than one tie
            else:
                d = Dice(1, 20, False)
                tiebreakers: List[int] = []
                for i in range(len(targets) + 1):
                    v, s = d.roll()
                    while v in tiebreakers:
                        v, s = d.roll()
                    tiebreakers.append(v)
                for i in range(len(tiebreakers) - 1):
                    targets[i].initiative_tiebreaker = tiebreakers[i]
                p.initiative_tiebreaker = tiebreakers[-1]
                
        self.players.append(p)
        self.players.sort(reverse=True, key=lambda x: x.initiative * 10 + x.initiative_tiebreaker)
    
    def get_order_as_string(self):
        if len(self.players) == 0:
            return 'Não existem jogadores atualmente nesta batalha'
        final = '```'
        i = 0
        for player in self.players:
            i += 1
            final += f'{i} - {player.name} - {player.initiative} {f"desempate (d20): {player.initiative_tiebreaker}" if player.initiative_tiebreaker > 0 else ""}\n'
        return final + '```'

class BattleCommands(Cog):

    battles: Dict[Any, List[Battle]]

    def __init__(self, bot) -> None:
        self.bot = bot
        self.battles = {}

    def find_battle(self, ctx: Context, name: str):
        if ctx.channel not in self.battles:
            return None
        
        channel_battles = self.battles[ctx.channel]
        battles = [x for x in channel_battles if x.name == name]
        
        return battles[0] if len(battles) > 0 else None


    @commands.command(name = 'battlecreate', aliases = ['bc'])
    async def start_battle(self, ctx: Context):
        """
            Command to start the battle, battles are bound by channel and name, the creation is as:

                .bc <NAME>

            If more than one word is gives as the name only the first word will be considered.
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) <= 0:
            await ctx.channel.send(ctx.author.mention + " você precisa definir um nome para a batalha")
            return
        
        if len(args) > 1:
            await ctx.channel.send(f'Foram inseridas mais de uma palavra, o nome da batalha será "{args[0]}"')

        search = self.find_battle(ctx, args[0])
        if search is not None:
            await ctx.channel.send(ctx.author.mention + " este nome de batalha já existe neste canal")
            return

        if ctx.channel in self.battles:
            self.battles[ctx.channel].append(Battle(args[0]))
        else:
            self.battles[ctx.channel] = [Battle(args[0])]

        await ctx.channel.send(ctx.author.mention + " Batalha criada!")

    
    @commands.command(name = 'battlejoin', aliases = ['bj'])
    async def battle_join(self, ctx: Context):
        """
            Command to join the battle, can be used as:

                .bj <BATTLE NAME> <PLAYER NAME> <INITIATIVE DICE>?

            If the INITIATIVE DICE is ommited there will be used a single d20. 
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) < 2:
            await ctx.channel.send(ctx.author.mention + " argumentos inválidos, uso: .bj <BATTLE NAME> <PLAYER NAME> <INITIATIVE DICE>?")
            return

        search = self.find_battle(ctx, args[0])
        if search is None:
            await ctx.channel.send(ctx.author.mention + " batalha não encontrada")
            return
        
        if search.find_player(args[1]) is not None:
            await ctx.channel.send(ctx.author.mention + " já existe um jogador com este nome nesta batalha")
            return
        
        initiative: int = 0
        roll_str: str = ''
        try:
            if len(args) >= 3:
                possible_dice = ''.join(args[2:])
                dices, values = split_input_into_dices(possible_dice)
                initiative, roll_str = roll_and_join_dices_and_numbers(dices, values)
            else:
                dice = Dice(1, 20, False)
                initiative, roll_str = roll_and_join_dices_and_numbers([dice], [])
        except (ValueError, AttributeError) as e:
            await ctx.channel.send(ctx.author.mention + " **Erro ao executar o comando:** " + str(e))
            return

        search.add_player(BattlePlayer(args[1], initiative))
        await ctx.channel.send(f'{ctx.author.mention} "{args[1]}" foi adicionado com sucesso à batalha "{search.name}", rolando {roll_str}')
    
    @commands.command(name = 'battleshow', aliases = ['bs'])
    async def battle_show(self, ctx: Context):
        """
            Command to show the initiative order in the battle:

                .bs <BATTLE NAME>
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) != 1:
            await ctx.channel.send(ctx.author.mention + " argumentos inválidos, uso: .bs <BATTLE NAME>")
            return
        
        search = self.find_battle(ctx, args[0])
        if search is None:
            await ctx.channel.send(ctx.author.mention + " batalha não encontrada")
            return
        
        await ctx.channel.send(search.get_order_as_string())
    
    @commands.command(name = 'battleremove', aliases = ['br'])
    async def battle_remove(self, ctx: Context):
        """
            Command to remove the battle:

                .br <BATTLE NAME>
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) != 1:
            await ctx.channel.send(ctx.author.mention + " argumentos inválidos, uso: .br <BATTLE NAME>")
            return
        
        search = self.find_battle(ctx, args[0])
        if search is None:
            await ctx.channel.send(ctx.author.mention + " batalha não encontrada")
            return
        
        self.battles[ctx.channel].remove(search)
        await ctx.channel.send(ctx.author.mention + " batalha removida!")
    
    @commands.command(name = 'battlelist', aliases = ['bl'])
    async def battle_list(self, ctx: Context):
        """
            Command to remove the battle:

                .bl
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) != 0:
            await ctx.channel.send(ctx.author.mention + " argumentos inválidos, uso: .bl")
            return
        
        if ctx.channel not in self.battles or len(self.battles[ctx.channel]) == 0:
            await ctx.channel.send(ctx.author.mention + " não existem batalhas neste canal atualmente")
            return
        battles = self.battles[ctx.channel]

        message = 'Batalhas atualmente em curso: ```\n'
        for battle in battles:
            message += f'{battle.name}\n'
        await ctx.channel.send(f'{ctx.author.mention} {message}```')
    
    @commands.command(name = 'battlekill', aliases = ['bk'])
    async def battle_kill(self, ctx: Context):
        """
            Command to join the battle, can be used as:

                .bk <BATTLE NAME> <PLAYER NAME> 
        """
        args = ctx.message.content.split(" ")[1:]

        if len(args) < 2:
            await ctx.channel.send(ctx.author.mention + " argumentos inválidos, uso: .bk <BATTLE NAME> <PLAYER NAME>")
            return

        search = self.find_battle(ctx, args[0])
        if search is None:
            await ctx.channel.send(ctx.author.mention + " batalha não encontrada")
            return
        
        player_search = search.find_player(args[1])
        if player_search is None:
            await ctx.channel.send(ctx.author.mention + " não existe ninguém com este nome nesta batalha")
            return

        search.players.remove(player_search)
        await ctx.channel.send(f'{ctx.author.mention} "{args[1]}" foi removido com sucesso da batalha "{search.name}"')

def setup(bot):
    bot.add_cog(BattleCommands(bot))