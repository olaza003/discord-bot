from ast import Not
import json
from urllib import response
import discord 
from tictactoe import *
from discord.ext import commands 

intents = discord.Intents.default()
intents.message_content = True
intents.messages=True
#client = discord.Client(intents=intents, ssl=False)
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
game = None
players = []
startValid = False


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global game, startValid

    if message.author == client.user:
        return
    if game is not None:
        await message.channel.send(f'Player {game.playerVal + 1} turn')

    if str(message.content) == '!startgame':
        if game is not None:
            await message.channel.send('a game is in progress!!!')
        else:
            game = tictactoe()
            await message.channel.send('Starting new game')
            await message.channel.send('Player 2 go ahead and type \'!AddMe\' to include 2nd player')
            players.append(str(message.author))
            #await message.channel.send('Enter value starting from 1 - 9')
            #game.gameRunning()
    elif game is not None and not startValid and str(message.content) == '!AddMe':
        print(players)
        if str(message.author) in players:
            await message.channel.send('player is already in the game')
        else:
            startValid = True
            await message.channel.send('Adding second player')
            players.append(message.author)
    elif game is not None and startValid and message.content.isdigit():
        player_input = int(message.content)
        
        if game.playerInputs(player_input): # if input is valid
            await message.channel.send(game.printBoard())
            if game.gameWin(): #check win status
                await message.channel.send(f"Player {game.playerVal + 1} WINS!!!")
                game.resetGame()
                game = None
            elif game.gameTie():
                await message.channel.send("Game Tied, No One Wins")
                game.resetGame()
                game = None
            game.changePlayer()
        else:
            await message.channel.send('Invalid input')
            await message.channe.send(f"waiting for player {game.playerVal + 1}'s turn")

    elif game is not None and str(message.content) == '!endgame':
        game.resetGame()
        game = None
        await message.channel.send("game has terminated")

        
    #username = str(message.author)
    #user_message = str(message.content)
    #channel = str(message.channel)
    
    #print(f"{username} said: '{user_message}' ({channel})")

    #if user_message == 'hello':
        #response = "HELLO!!"
        #await message.channel.send(response) #if is_private else await message.channel.send(response)
        

with open('config.json') as f:
    data = json.load(f)

token = data['token']

client.run(token) 
