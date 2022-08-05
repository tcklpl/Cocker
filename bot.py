from discord.ext import commands
from bot_token import token

bot = commands.Bot(command_prefix='.')

cogs = ['commands.help', 'commands.roll', 'commands.boundaries', 'commands.playerdices', 'commands.battle']

for cog in cogs:
    bot.load_extension(cog)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

bot.run(token)