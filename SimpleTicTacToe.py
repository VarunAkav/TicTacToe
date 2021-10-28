# This file contains the game play
import math

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
        return int(input("{name}, select the cell to place the marker(0-8): ".format(name = self.name)))

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
    
    def showBoard(self):
        print('{} | {} | {}'.format(self.squares[6].value,self.squares[7].value,self.squares[8].value))
        print('---------')
        print('{} | {} | {}'.format(self.squares[3].value,self.squares[4].value,self.squares[5].value))
        print('---------')
        print('{} | {} | {}'.format(self.squares[0].value,self.squares[1].value,self.squares[2].value))
    
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
        if self.winner == None:
            print('The game was a draw')
        else:
            print('The winner of the game is {}!'.format(
                    list(filter(lambda x: x.marker == self.winner,(self.px,self.po)))[0].name)
                )
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
        newBrd = Board()
        for sq in range(9):
            newBrd.squares[sq].value = self.squares[sq].value
        newBrd.turn = self.turn
        newBrd.movesPlayed = self.movesPlayed
        return newBrd


class BotPlayer(Player):
    def __init__(self,board:Board,marker:str):
        self.board = board
        self.marker = marker
        
    def findWinningCases(self,board):
        pass

    def sendMove(self):
        pass

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
    P2 = Player(input('Enter the name of Player 2: '),'o')
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
