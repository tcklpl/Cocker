# Cocker
Cocker is a Discord bot to roll dices and do simple (plus or minus) operations with or without the dices.

## Commands
Command    | Syntax                                            | RegEx Formatting                            | Explanation
-----------|---------------------------------------------------|---------------------------------------------|-------------
Roll       | .r <*dice and/or numbers to sum and/or subtract*> | ([+-]{0,1}[0-9]*d[0-9]+)\|([+-]{0,1}[0-9]+) | Rolls the informed dices and performs any necessary addition or subtraction with the values.
Boundaries | .b <*dice and/or numbers to sum and/or subtract*> | ([+-]{0,1}[0-9]*d[0-9]+)\|([+-]{0,1}[0-9]+) | Informs the minimum and maximum possible values you can get with the informed dices and values.
Player Dices| .pd                                              | | Rolls 6 * 4d6 and subtracts the smallest dice from every roll.
Help       | .h                                                |                                             | Shows the help message containing all available commands.
Create Battle | .bc <*battle name*> | \w+ | Creates a battle with the specified name.
Join Battle | .bj <*battle name*> <*player name*> (<*initiative dice*>)? | \w+ \w+ ([+-]{0,1}[0-9]*d[0-9]+)\|([+-]{0,1}[0-9]+) | Joins the specified battle with the required name. The initiative dice is optional, if omitted it will default to a d20.
Kill (Leave Battle) | .bj <*battle name*> <*player name*> | \w+ \w+ | Removes the specified player from the battle.
Show Battle | .bs <*battle name*> | \w+ | Lists all the players in the specified battle sorted by the initiative.
Remove Battle | .br <*battle name*> | \w+ | Removes the specified battle.

> **Battles are channel bound**. If you start a battle on the channel #a, the battle can only be interacted inside this channel, messages on channel #b will report the battle as non-existent.

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

## Running
You need to create a file named `bot_token.py` with your bot token:
```
token = "<YOUR BOT TOKEN>"
```
After this, you can just run the bot with
```
python3 bot.py
```
## Yeah, but WHY cocker?
idk

Also, the bot has a 5% chance of not doing anything and telling you to go fuck yourself.
