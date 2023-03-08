import json
import discord 
import responses
from discord.ext import commands 

intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents, ssl=False)
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' ({channel})")

    if user_message == 'hello':
        response = responses.handle_response("HELLO!!")
        await message.author.send(response)

with open('config.json') as f:
    data = json.load(f)

token = data['token']

client.run(token)