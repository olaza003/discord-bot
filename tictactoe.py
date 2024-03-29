
# tictactoe game -> utilize discord to play after this project is utilize

#create board
from operator import truediv
import math


class tictactoe(object):
    board = [[None, None, None ],
            [None, None, None],
            [None, None, None]]
    player = ["X", "O"]
    playerVal = 0 # 0 : X | 1 : O
    GameStatus = False # true : someone win or tie | false : ongoing game
    inputs = 0

    #checker:
    def checkDiagonal(self):
        if self.board[1][1] != None and (self.board[0][0] == self.board[1][1] == self.board[2][2]
            or self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return True
        return False
    #   check diagonal
    #   check horizontal --
    def checkHorizontal(self):
        for i in range(len(self.board)):
            if self.board[i][0] != None and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return True
        return False
    #   check vertical |
    def checkVertical(self):
        for i in range(len(self.board[0])):
            if self.board[0][i] != None and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return True
        return False

    #check input player
    #   add in inputs
    #   also check if in bounds
    def playerInput(self): # 1 - 9 
        inp = int(input("Enter a value: "))
        inp -= 1
        row = inp // 3 
        col = inp % 3
        if inp >= 0 and inp < 9 and self.board[row][col] == None:
            self.board[row][col] = self.player[self.playerVal]
            self.inputs += 1
            return True

        print("invalid input!")
        return False

    def playerInputs(self, num): # 1 - 9 with input
        inp = num  - 1
        row = inp // 3 
        col = inp % 3
        if inp >= 0 and inp < 9 and self.board[row][col] == None:
            self.board[row][col] = self.player[self.playerVal]
            return True

        print("invalid input!")
        return False

    #check if win or tie: 
    #   utilize checker

    def printBoard(self):
        strBoard = ""
        for i in range(len(self.board)):
            for k in range(len(self.board[0])):
                strBoard += " "
                if self.board[i][k] is None:
                    strBoard += " "
                else:
                    strBoard += self.board[i][k]
                if k < 2:
                    strBoard += " | "
                else:
                    strBoard += "\n"
            if i < 2:
                strBoard += "-------------\n"
        print(strBoard)
        return strBoard

    def changePlayer(self): 
        if self.playerVal == 0:
            self.playerVal = 1
        else:
            self.playerVal = 0

    def gameWin(self):
        if self.checkDiagonal() or self.checkHorizontal() or self.checkVertical():
            return True
        return False

    def gameTie(self):
        if self.inputs == 9:
            return True
        return False

    def gameStatus(self):
        if self.gameWin():
            print(f"Player {self.player[self.playerVal]} win")
            return True
        if self.gameTie():
            print('Game tied!!! No One WINS!!!')
            return True
        return False

    def gameRunning(self):
        self.printBoard()
        validator = False
        while validator is False:
            playInput = self.playerInput()
            while playInput is False:
                playInput = self.playerInput()
            self.printBoard()
            validator = self.gameStatus()
            self.changePlayer()
        self.resetGame()

        print("reset game")
    
    #adding AI with MinMax algorithm
    def AIMove(self):
        bestScore = -math.inf
        bestMove = None
        for i in range(3):
            for k in range(3):
                if self.board[i][k] is None:
                    self.board[i][k] = self.player[1]
                    score = self.minimax(0, self.playerVal == 1)
                    self.board[i][k] = None
                    if score > bestScore:
                        bestScore = score
                        bestMove = (i,k)
        if bestMove is not None:
            self.board[bestMove[0]][bestMove[1]] = self.player[1]
        else:
            print("Game tied!!! No One WINS!!!")

    def minimax(self, depth, isMaximizing):
        if self.gameWin():
            if self.playerVal == 1:
                return 1
            else:
                return -1
        if self.gameTie():
            return 0
        if isMaximizing:
            bestScore = float('-inf')
            for i in range(3):
                for k in range(3):
                    if self.board[i][k] is None:
                        self.board[i][k] = self.player[1]
                        score = self.minimax(depth+1, not isMaximizing)
                        self.board[i][k] = None
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = float('inf')
            for i in range(3):
                for k in range(3):
                    if self.board[i][k] is None:
                        self.board[i][k] = self.player[0]
                        score = self.minimax(depth+1, not isMaximizing)
                        self.board[i][k] = None
                        bestScore = min(score, bestScore)
            return bestScore

    def resetGame(self):
        self.board = [[None for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        self.inputs = 0
        self.playerVal = 0
    
    def AIGameplay(self):
        self.printBoard()
        validator, currPlayer = False, False
        while validator is False:
            if currPlayer is False:
                playerInput = self.playerInput()
                while playerInput is False:
                    playerInput = self.playerInput()
            else:
                playerInput = self.AIMove()
            self.printBoard()
            if self.gameTie() or self.gameWin():
                validator = True
                if currPlayer:
                    print('AI wins!!!')
                else:
                    print('You win')
            currPlayer = not currPlayer
        self.resetGame()
        print('Reset game')



if __name__ == '__main__':
    play = tictactoe()
    gameMode = input('1 vs 1 : (1) or VS. AI (2)')
    if gameMode == 1:
        play.gameRunning()
    else:
        play.AIGameplay()
    print("test")
