import re, random
from dice import Dice

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

def check_if_will_execute() -> bool:
    return random.randint(1, 100) <= 5