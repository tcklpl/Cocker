from typing import List
from dice import Dice


def roll_and_join_dices_and_numbers(dice_arr: List[Dice], simple_numbers: List[int]):

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
            
        
        final_str += f'**{str(total)}**'

        # If the player rolls a single d20 (with or without bonuses/nerfs) and gets a value <= 1
        if total <= 1 and len(dice_arr) == 1 and dice_arr[0].size == 20:
            final_str += " kkkkkkkkkkk se fodeu"

        return total, final_str