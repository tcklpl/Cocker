# Cocker
Cocker is a Discord bot to roll dices and do simple (plus or minus) operations with or without the dices.

## Commands
Command    | Syntax                                            | RegEx Formatting                            | Explanation
-----------|---------------------------------------------------|---------------------------------------------|-------------
Roll       | .r <*dice and/or numbers to sum and/or subtract*> | ([+-]{0,1}[0-9]*d[0-9]+)\|([+-]{0,1}[0-9]+) | Rolls the informed dices and performs any necessary addition or subtraction with the values.
Boundaries | .b <*dice and/or numbers to sum and/or subtract*> | ([+-]{0,1}[0-9]*d[0-9]+)\|([+-]{0,1}[0-9]+) | Informs the minimum and maximum possible values you can get with the informed dices and values.
Help       | .h                                                |                                             | Shows the help message containing all available commands.

## Dice formatting
The dice is formatted as:
> [0-9]*d[0-9]+

That means:
* You **do not** need to specify the ammount of dices being rolled. It will default to 1.
* You **need** to specify the dice maximum value. This value doesn't need to reflect a real dice, you can have any x-faced dice (of course, with x > 0).

The following **are** valid dices:
* 2d100
* d6
* 1d8

The following **ARE NOT** valid dices:
* d
* 0d8
* d0
* d-1

## Yeah, but WHY cocker?
idk
