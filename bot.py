import discord, random, re
from discord.ext import commands
from bot_token import token

client = discord.Client()

class Dice:
    def __init__(self, quant: int, size: int, negative: bool):
        if quant <= 0 or size <= 0:
            raise AttributeError("Dado com quantidade e/ou valor negativo")

        self.quant = quant
        self.size = size
        self.negative = negative
        self.total = 0
        self.roll_str = ('-' if negative else '') + str(quant) + "d" + str(size)

    def roll(self):
        self.roll_str += " ( "
        for i in range(self.quant):
            this_roll = random.randint(1, self.size)
            self.total += this_roll
            self.roll_str += str(this_roll) + " "
        self.roll_str += ")"
        if self.negative:
            self.total *= -1
        return self.total, self.roll_str

    def boundaries(self):
        return self.quant, self.quant * self.size

def split_raw_input_into_dices(raw_input):
    input_without_command = ("".join(raw_input.split( )[1:])).replace(" ", "").lower()
    input_splitted_into_dices_and_numbers = re.findall('([+-]{0,1}[0-9]*d[0-9]+)|([+-]{0,1}[0-9]+)', input_without_command)

    if len(input_splitted_into_dices_and_numbers) == 0:
        raise ValueError("Input mal formatada")

    dices = []
    simple_values = []

    for arg in input_splitted_into_dices_and_numbers:
        possible_dice   = arg[0]
        possible_number = arg[1]

        if possible_dice != '' and possible_number != '':
            raise ValueError("Valor mal formatado: `" + arg + "`")

        if possible_dice != '':
            possible_dice_regex = re.search('^[+-]{0,1}([0-9]*)d([0-9]+)$', possible_dice)

            if possible_dice_regex is None:
                raise ValueError("Dado inválido: `" + possible_dice + "`")

            quant    = possible_dice_regex.group(1) if possible_dice_regex.group(1) != '' else 1
            size     = int(possible_dice_regex.group(2))
            negative = '-' in possible_dice

            quant = int(quant)
            dices.append(Dice(quant, size, negative))
        else:
            simple_values.append(int(arg[1]))
    
    return dices, simple_values

def roll_and_join_dices_and_numbers(dice_arr, simple_numbers):

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

def get_roll_boundaries(dice_arr, simple_numbers):
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

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.r '):
        try:
            dices, simple_values = split_raw_input_into_dices(message.content)
            final = roll_and_join_dices_and_numbers(dices, simple_values)

            if len(final) >= 2000:
                raise ValueError("A resposta tem mais de 2k caracteres, oq caralhos tu ta tentando rolar?")

            await message.channel.send(message.author.mention + " " + final)
        except (ValueError, AttributeError) as e:
            await message.channel.send(message.author.mention + " **Erro ao executar o comando:** " + str(e))
    
    elif message.content.startswith('.b '):
        try:
            dices, simple_values = split_raw_input_into_dices(message.content)
            min, max = get_roll_boundaries(dices, simple_values)

            await message.channel.send(message.author.mention + " Você pode rolar isso entre {} e {}".format(str(min), str(max)))
        except (ValueError, AttributeError) as e:
            await message.channel.send(message.author.mention + " **Erro ao executar o comando:** " + str(e))
    
    elif message.content == '.h':
            await message.channel.send(message.author.mention + " Comandos:\n```.r <dados> : rola os dados\n.b <dados> : mostra o mínimo e máximo que é possível tirar com os dados informados.\n.h         : mostra essa mensagem.```")

client.run(token)