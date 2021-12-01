import random

class Dice:
    def __init__(self, quant: int, size: int, negative: bool):
        if quant <= 0 or size <= 0:
            raise AttributeError("Dado com quantidade e/ou valor negativo")

        self.quant = quant
        self.size = size
        self.negative = negative
        self.total = 0
        self.min_roll = self.quant * self.size
        self.roll_str = ('-' if negative else '') + str(quant) + "d" + str(size)

    def roll(self):
        self.roll_str += " ( "
        for i in range(self.quant):
            this_roll = random.randint(1, self.size)
            if this_roll <= self.min_roll:
                self.min_roll = this_roll
            self.total += this_roll
            self.roll_str += str(this_roll) + " "
        self.roll_str += ")"
        if self.negative:
            self.total *= -1
        return self.total, self.roll_str
    
    def get_as_character_dices(self):
        self.roll()
        self.total -= self.min_roll
        self.roll_str += " - " + str(self.min_roll)
        return self.total, self.roll_str


    def boundaries(self):
        return self.quant, self.quant * self.size