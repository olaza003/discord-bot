import discord 
from discord.ext import commands 

intents = discord.Intents.default()
client = discord.Client(intents=intents, ssl=False)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run('OTQzNzg0Mzk1MTkyNTYxNzA1.GKOdDf.eotOpoU20x1a0aLhj6zbw9i9hXHLkHKKo6eGQM')