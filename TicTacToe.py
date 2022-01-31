# This file contains the game play
import math
from functools import reduce
import random

class Square:
    def __init__(self):
        self.value = ' '
        self.pos = None

    def setVal(self,ch:str):
        self.value = ch if ch in ('x','o') else self.value
    
class Player:
    def __init__(self,name:str,marker:str):
        self.name = name
        self.marker = marker

    def sendMove(self):
        player_input = int(input("{name}, select the cell to place the marker(0-8): ".format(name = self.name)))
        if player_input in range(0,9):
            return player_input
        print("Please enter a number from 0-8")
        return self.sendMove()

    def getBoard(self,board):
        print('#############')
        print('# {} | {} | {} #'.format(board.squares[6].value,board.squares[7].value,board.squares[8].value))
        print('#-----------#')
        print('# {} | {} | {} #'.format(board.squares[3].value,board.squares[4].value,board.squares[5].value))
        print('#-----------#')
        print('# {} | {} | {} #'.format(board.squares[0].value,board.squares[1].value,board.squares[2].value))
        print('#############')
class Board:
    def __init__(self,px:Player,po:Player):
        self.gameOn = False
        self.winner = None
        # self.turn = 'x'
        self.px = px; self.po = po
        self.playerTurn = self.px
        self.movesPlayed = 0

        self.squares = [Square() for i in range(9)]
        pos = 0
        for square in self.squares:
            square.pos = pos
            pos += 1
    
    def checkWinner(self):
        # Checking for winners
        for sq in [0,3,6]:
            if (self.squares[sq].value == self.squares[sq+1].value == self.squares[sq+2].value) and self.squares[sq].value != ' ':
                self.winner = self.squares[sq].value
                self.gameOn = False
                return
        for sq in [0,1,2]:
            if (self.squares[sq].value == self.squares[sq+3].value == self.squares[sq+6].value) and self.squares[sq].value != ' ':
                self.winner = self.squares[sq].value
                self.gameOn = False
                return
            
        if (self.squares[2].value == self.squares[4].value == self.squares[6].value) and self.squares[2].value != ' ':
            self.winner = self.squares[2].value
            self.gameOn = False
            return
        if (self.squares[0].value == self.squares[4].value == self.squares[8].value) and self.squares[0].value != ' ':
            self.winner = self.squares[0].value
            self.gameOn = False
            return
        for square in self.squares:
            if square.value == ' ':
                return
        self.winner = ''            # Indicating Draw
    
    def showBoard(self):
        self.playerTurn.getBoard(self)
        # print('{} | {} | {}'.format(self.squares[6].value,self.squares[7].value,self.squares[8].value))
        # print('---------')
        # print('{} | {} | {}'.format(self.squares[3].value,self.squares[4].value,self.squares[5].value))
        # print('---------')
        # print('{} | {} | {}'.format(self.squares[0].value,self.squares[1].value,self.squares[2].value))
    
    def playMove(self,sq: int):
        if self.squares[sq].value == ' ':
            self.squares[sq].setVal(self.playerTurn.marker)
            # self.turn = list(filter(lambda x: x != self.turn,('x','o')))[0]
            self.playerTurn = list(filter(lambda x: x != self.playerTurn,(self.px,self.po)))[0] # Toggling players
            self.movesPlayed += 1
            self.checkWinner()
    
    def getMove(self):
        return self.playerTurn.sendMove()

    def showResult(self):
        if self.winner == '':
            print('The game was a draw')
        else:
            print('The winner of the game is {}!'.format(
                    list(filter(lambda x: x.marker == self.winner,(self.px,self.po)))[0].name)
                )       ### Change this
        self.winner = None

    def play(self):
        
        self.showBoard()

        self.gameOn = True
        while self.gameOn and self.movesPlayed < 9:
            self.playMove(self.getMove())
            self.showBoard()
            # self.checkWinner()
        self.showResult()
        self.gameOn = False
    
    def copyBoard(self):
        newBrd = Board(self.px,self.po)
        for sq in range(9):
            newBrd.squares[sq].value = self.squares[sq].value
        newBrd.playerTurn = self.playerTurn
        newBrd.movesPlayed = self.movesPlayed
        return newBrd


class BotPlayer(Player):
    def __init__(self,marker:str):
        # Player.__init__('Akari',marker)
        self.name = 'Akari'
        self.marker = marker
    
    def getBoard(self, board):
        self.board = board

    def findBoardScores(self,board:Board):
        if board.winner:
            return -1
        if board.winner == '':
            return 0
        
        nxtMoves = self.findAllPossibleNxtMoves(board)
        nxtScores = []
        for nxtBoard in nxtMoves:
            nxtScores.append(self.findBoardScores(nxtBoard))
        
        if board.playerTurn == self:
            return -min(nxtScores)/len(nxtMoves)
        return -reduce(lambda x,y: x+y,nxtScores)/len(nxtMoves)

    def sendMove(self):
        nxtMoves = self.findAllPossibleNxtMoves(self.board)
        nxtScores = []
        for nxtBoard in nxtMoves:
            nxtScores.append(self.findBoardScores(nxtBoard))
        # print("Akari: list of possible scores is: ",nxtScores)

        bestScore = min(nxtScores)
        # print('Akari: Best score is')
        bestScoreMoves = []
        for mv,score in enumerate(nxtScores):
            if score == bestScore:
                bestScoreMoves.append(mv)
        
        nxtMove = bestScoreMoves[random.randrange(0,len(bestScoreMoves))]
        possibleMoves = []
        for sq in range(9):
            if self.board.squares[sq].value == ' ':
                possibleMoves.append(sq)
        return possibleMoves[nxtMove]

    def findAllPossibleNxtMoves(self,board:Board):
        if board.winner != None:
            return []
        listOfMoves = []
        for sq in range(9):
            if board.squares[sq].value == ' ':
                newBrd = board.copyBoard()
                newBrd.playMove(sq)
                listOfMoves.append(newBrd)
        return listOfMoves


#######################

def gameStart():
    P1 = Player(input('Enter the name of Player 1: '),'x')
    if P1.name == '_Akari':
        P1 = BotPlayer('x')
    P2 = Player(input('Enter the name of Player 2: '),'o')
    if P2.name == '_Akari':
        P2 = BotPlayer('o')

    Brd = Board(P1,P2)
    Brd.play()

gameStart()
# Brd.playMove(0)
# newBrd = Brd.copyBoard()
# newBrd.showBoard()
# print('########################')
# newBrd.playMove(1)
# newBrd.showBoard()
# print('########################')
# Brd.showBoard()
