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
startValid, startGame = False, False
gameMode = 0 # (1) PVP (diff) | (2) PVP (Same) | (3) P V AI
instruct = '' #will be the last instruction pushed
counter = 0 #player

async def Instruction(message, cont):
    await message.channel.send(cont)

def changeCounter():
    counter = 0 if counter == 1 else 0

def resetWholeGame():
    game.resetGame()
    game = None
    startValid, startGame = False, False
    gameMode, counter = 0, 0
    instruct = ''

async def TypeGameMessage(message):
    instructString = 'Pick type of game play:\n' \
                    '(1) PVP (different player)\n' \
                    '(2) PVP (same player)\n' \
                    '(3) PVE (AI)\n'   
    await message.channel.send(instructString)
    return instructString

async def FirstGameMode(message):
    global game
    if message.content.isdigit() and str(message.author) == players[counter]:
        player_input = int(message.content)
        if game.playerInputs(player_input): #check if input is valid
            changeCounter()
            await message.channel.send(game.printBoard())
            if game.gameWin():
                await message.channel.send(f'Player {counter + 1} wins!!!')
                resetWholeGame()
            elif game.GameTie():
                await message.channle.send('Game tied, no one wins!!!')
                resetWholeGame()
        else:
            instruct = 'Invalid input'
            await message.channel.send(instruct)
    elif str(message.author) in players and str(message.author) != players[counter]:
        instruct = 'either what is inputted is valid or the player '
        await message.channel.send(instruct)
                
async def SecondGameMode(message):
    global game
    if message.content.isdigit() and game.playerInputs(int(message.content)):
        await message.channel.send(game.printBoard())
        if game.gameWin():
            await message.channel.send(f"Player {game.playerVal + 1} WINS!!!")
            game.resetGame()
            game = None
        elif game.gameTie():
            await message.channel.send("Game Tied, No one wins")
            game.resetGame()
            game = None
        else:
            game.changePlayer()
    else:
        instruct = f'Invalid input \n{game.playerVal + 1}\'s turn'
        await message.channel.send(instruct)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global game, startValid, gameMode

    if message.author == client.user:
        return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    
    print(f"{username} said: '{user_message}' ({channel})")

    #check what kind of game mode
    # (1) player vs player : Different ID's
    # (2) player vs player : same ID
    # (3) player vs AI
    if str(message.content) == '!Startgame':
        if not startValid and game is not None:
            await message.channel.send('Unable to start, follow instruction')
            await Instruction(message, instruct)
        else:
            game = tictactoe()
            instruct = await TypeGameMessage(message)
            players.append(str(message.author))
    #starting game
    elif game and not startValid and message.content.isdigit():
        player_choice = int(message.content)
        if player_choice == 1: #pvp (diff)
            await message.channel.send('Initiating game')
            gameMode = int(message.content)
            startValid = True
            players.append(str(message.author))
            instruct = 'Player 2 type !AddMe to add player and start game'
            await Instruction(message, instruct)
        elif player_choice == 2: #pvp (self)
            await message.channel.send('Starting game, playing with self')
            gameMode = int(message.content)
            startValid = True
            players.append(str(message.author))
        elif player_choice == 3:
            await message.channel.send('Starting game with AI')
            gameMode = int(message.content)
            startValid = True
            players.append(str(message.author))
        else:
            await message.channel.send('Wrong input')
            await Instruction(message, instruct)

    elif str(message.content) == '!AddMe' and gameMode == 1 and len(players) == 1:
        players.append(str(message.author))
        await message.channel.send("Starting game")
        await message.channel.send("Player 1 go ahead and enter a number")
    
    elif startValid and gameMode == 1 and len(players) == 2:
        #check if current player matches with the expected one
        await FirstGameMode(message)
    elif startValid and gameMode == 2:
        await SecondGameMode(message)
    elif startValid and gameMode == 3:
        pass #implement AI
    elif game is not None and str(message.content) == '!endgame':
        resetWholeGame()
        await message.channel.send("game has terminated")
        instruct = ''
    

with open('config.json') as f:
    data = json.load(f)

token = data['token']

client.run(token) 

