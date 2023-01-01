## 20181227 HojinKim ##
## MiniMax TicTacToe ##
# Project 1: Win the TicTacToe Game

## -- Library ------------------------------------ ##
import pygame
import os
import numpy as np

## -- Variable ----------------------------------- ##
# Window related
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# BoardCell related
BOARD_TOP = 100
BOARD_LEFT = 500
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
BOARD_COLUMNS = 3
BOARD_ROWS = 3

CELL_WIDTH = BOARD_WIDTH / BOARD_COLUMNS
CELL_HEIGHT = BOARD_HEIGHT / BOARD_ROWS

## - Class ---------------------------------------- ##
class BoardCell:
    def __init__(self, _locationNum, _x, _y):
        self.locationNum = _locationNum
        self.owner = 0 # 0:None / 1:O / 2:X
        self.x = _x
        self.y = _y

    def isPressed(self, _pos):
        if _pos[0] > self.x and _pos[0] < self.x + CELL_WIDTH and _pos[1] > self.y and _pos[1] < self.y + CELL_HEIGHT:
            # Pressed
            return True
        else:
            # Not Pressed
            return False
    
    def getLocation(self,):
        return self.locationNum
    
    def setOwner(self, _owner):
        if _owner and self.owner == 0:
            if _owner == 1 or _owner == 'O':
                self.owner = 1
            elif _owner == 2 or _owner == 'X':
                self.owner = 2
    
    def draw(self,_screen):
        #pygame.draw.rect(_screen, (255,255,255), [self.x, self.y, CELL_WIDTH, CELL_HEIGHT], 4)
        _screen.blit(imgArr[self.owner], [self.x, self.y])

class Button:
    def __init__(self, _displayVal, _returnVal, _x, _y, _width, _height):
        self.displayVal = _displayVal
        self.returnVal = _returnVal
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height

    def isPressed(self, _pos, _isActive):
        if _pos[0] > self.x and _pos[0] < self.x + self.width and _pos[1] > self.y and _pos[1] < self.y + self.height and _isActive:
            # Pressed
            return self.returnVal
        else:
            # Not Pressed
            return 0
    
    def draw(self, _screen, _isActive):
        if _isActive:
            pygame.draw.rect(_screen, (255,255,255), [self.x, self.y, self.width, self.height], 4)
            _screen.blit(font_norm.render(str(self.displayVal), True, (255,255,255)), [self.x+self.width/2-10, self.y+self.height/2-10])

## - Function -------------------------------------- ##
# - MiniMax related ------------------------- #
def minimax(_board, _depth, _isMaxComputer):
    positionNum = 0
    if _depth == 0 or not emptyArr(_board) or isEnd(_board):
        return 0, evaluate(_board) # end of tree, now pass this to upper tree
    if _isMaxComputer: # Ai's turn - maximize
        value = -99
        for locationNum in emptyArr(_board):
            board_copy = _board.copy()
            board_copy[locationNum] = computerLetter
            _, score = minimax(board_copy, _depth - 1, False)
            if score > value: # maximum value found
                value = score
                positionNum = locationNum
            if _depth == 9:
                print("Looking for Maximum - " + str(locationNum) + " : " + str(score))
            if score == 1: # calculation is meaningless when player already wins
                break
    else: # Player's turn - minimize
        value = 99
        for locationNum in emptyArr(_board):
            board_copy = _board.copy()
            board_copy[locationNum] = playerLetter
            _, score = minimax(board_copy, _depth - 1, True)
            if score < value: # minimal value found
                value = score
                positionNum = locationNum
            if score == -1: # calculation is meaningless when computer already loses
                break
    if _depth == 9:
        print()
    return positionNum, value

def evaluate(_board):
    if isWinner(_board, computerLetter):
        score = 1
    elif isWinner(_board, playerLetter):
        score = -1
    else:
        score = 0
    return score

def emptyArr(_board):
    emptyNumBoard = []
    for locationNum in range(1, len(_board)):
        if isSpaceFree(_board, locationNum):
            emptyNumBoard.append(locationNum)
    if len(emptyNumBoard) != 0:
        return emptyNumBoard
    else:
        return 0

def isEnd(_board):
    return isWinner(_board, playerLetter) or isWinner(_board, computerLetter)

def isWinner(_board, _owner):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use _board instead of board and _owner instead of letter so we don't have to type as much.
    return ((_board[7] == _owner and _board[8] == _owner and _board[9] == _owner) or # across the top
    (_board[4] == _owner and _board[5] == _owner and _board[6] == _owner) or # across the middle
    (_board[1] == _owner and _board[2] == _owner and _board[3] == _owner) or # across the bottom
    (_board[7] == _owner and _board[4] == _owner and _board[1] == _owner) or # down the left side
    (_board[8] == _owner and _board[5] == _owner and _board[2] == _owner) or # down the middle
    (_board[9] == _owner and _board[6] == _owner and _board[3] == _owner) or # down the right side
    (_board[7] == _owner and _board[5] == _owner and _board[3] == _owner) or # diagonal
    (_board[9] == _owner and _board[5] == _owner and _board[1] == _owner)) # diagonal

def isSpaceFree(_board, _locationNum):
    # Return true if the passed move is free on the passed board.
    return _board[_locationNum] == ' '

# - Ingame related ------------------------- #
def inputPlayerLetter(_input):
    # the first element in the list is the player's letter, the second is the computer's letter.
    if _input == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if np.random.randint(2) == 0:
        return 'computer'
    else:
        return 'player'
    
def getPlayerMove(_board, _input):
    # Let the player type in their move.
    if isSpaceFree(_board, _input):
        return _input
    else:
        return 0

def getComputerMove(_board):
    # Given a board and the computer's letter, determine where to move and return that move.
    locationNum,_ = minimax(_board, 9, True)
    return locationNum

def makeMove(_board, _owner, _locationNum):
    _board[_locationNum] = _owner

def drawBoard(_screen):
    # This function prints out the board that it was passed.
    _screen.blit(boardImg, [BOARD_LEFT, BOARD_TOP])
    for cell in cellArr:
        cell.draw(_screen)

def explanation(_screen, _quote):
    _screen.blit(font_norm.render(str(_quote), True, (255,255,255)), [50, WINDOW_HEIGHT/2])
  
## -- Setup -------------------------------------- ##
# Pygame init
pygame.init()
pygame.display.set_caption("Pygame_template")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
# Asset path
assets_path = os.path.join(os.path.dirname(__file__), '_assets')

# Image init
imgArr = []
for i in range(3):
    tempImgName = str(i) + '.png'
    tempImg = pygame.image.load(os.path.join(assets_path, tempImgName))
    imgArr.append(tempImg)
boardImg = pygame.image.load(os.path.join(assets_path, 'board.png'))

# Class init (BoardCell)
cellArr = []
locNum = 1
for j in range(BOARD_ROWS):
    for i in range(BOARD_COLUMNS):
        x = BOARD_LEFT + i*CELL_WIDTH
        y = BOARD_TOP + (2-j)*CELL_HEIGHT
        tempKey = BoardCell(locNum, x, y)
        cellArr.append(tempKey)
        locNum += 1

# Class init (Button)
button_O = Button('O', 'O', 50, WINDOW_HEIGHT/2+50, 380, 60)
button_X = Button('X', 'X', 50, WINDOW_HEIGHT/2+120, 380, 60)

# Font init
font_small = pygame.font.SysFont('FixedSys', 20, True, False)
font_norm = pygame.font.SysFont('FixedSys', 40, True, False)
font_large = pygame.font.SysFont('FixedSys', 80, True, False)

# Sound init
click = pygame.mixer.Sound(os.path.join(assets_path, 'click.wav'))
tie = pygame.mixer.Sound(os.path.join(assets_path, 'tie.wav'))
lose = pygame.mixer.Sound(os.path.join(assets_path, 'lose.wav'))
win = pygame.mixer.Sound(os.path.join(assets_path, 'win.wav'))

# Stage selector init
stage = ('pregame', 'ingame', 'endgame')
currentStage = 'pregame'

# Game value init
theBoard = [' '] * 10
playerLetter = ''
computerLetter = ''
result = ('tie', 'win', 'lose')
gameResult = ''
turn = 'player'

## -- Update -------------------------------------- ##
done = False
frameTime = 0
while not done:
    # 마우스 위치 값 가져오기
    pos = pygame.mouse.get_pos()

    # 이벤트 반복 구간
    isClick = False
    input = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:    
            isClick = True
            click.play()
            if currentStage == 'pregame':
                if button_O.isPressed(pos, True):
                    input = button_O.isPressed(pos, True)
                if button_X.isPressed(pos, True):
                    input = button_X.isPressed(pos, True)
            elif currentStage == 'ingame':
                for cell in cellArr:
                    if cell.isPressed(pos) and cell.owner == 0:
                        cell.setOwner(playerLetter)
                        input = cell.getLocation()
            elif currentStage == 'endgame':
                if button_O.isPressed(pos, True):
                    input = button_O.isPressed(pos, True)
                if button_X.isPressed(pos, True):
                    input = button_X.isPressed(pos, True)
            
    # 윈도우 화면 채우기
    screen.fill((0,0,0))
        
    # 게임 로직 구간
    # Stage Selector
    #---------------------------------------------------#
    if currentStage == 'pregame': # Choose X or Y, Choose order
        # Reset the board
        theBoard = [' '] * 10
        explanation(screen, 'Do you want to be O or X?')
        button_O.draw(screen, True)
        button_X.draw(screen, True)
        if input == 'O' or input == 'X':
            playerLetter, computerLetter = inputPlayerLetter(input)
            turn = whoGoesFirst()
            currentStage = 'ingame' # Next Stage

    #---------------------------------------------------#
    elif currentStage == 'ingame': # Gameplay until someone wins or ties
        ##################
        if turn == 'player': # player turn
            if input != 0:
                move = getPlayerMove(theBoard, input)
                if move != 0:
                    makeMove(theBoard, playerLetter, move)
                if isWinner(theBoard, playerLetter):
                    gameResult = 'win'
                    win.play()
                    currentStage = 'endgame'
                else:
                    if not emptyArr(theBoard):
                        gameResult = 'tie'
                        tie.play()
                        currentStage = 'endgame'
                    elif move != 0:
                        turn = 'computer'
        ##################
        else: # computer turn
            move = getComputerMove(theBoard)
            debugFrame = frameTime
            cellArr[move-1].setOwner(computerLetter)
            makeMove(theBoard, computerLetter, move)
            if isWinner(theBoard, computerLetter):
                gameResult = 'lose'
                lose.play()
                currentStage = 'endgame'
            else:
                if not emptyArr(theBoard):
                    gameResult = 'tie'
                    tie.play()
                    currentStage = 'endgame'
                else:
                    turn = 'player'

    #---------------------------------------------------#
    elif currentStage == 'endgame': # Display game result, Ask to play again
        button_O.draw(screen, True)
        button_X.draw(screen, True)
        if gameResult == 'tie':
            explanation(screen, 'The game was Tie. Replay?')
        elif gameResult == 'win':
            explanation(screen, 'You Win! Replay?')
        elif gameResult == 'lose':
            explanation(screen, 'You Lose... Replay?')
        if input == 'O' or input == 'X':
            if input == 'O':
                # Reset values
                for cell in cellArr:
                    cell.owner = 0
                theBoard = [' '] * 10
                playerLetter = ''
                computerLetter = ''
                gameResult = ''
                currentStage = 'pregame'
            elif input == 'X':
                done = True # Next Stage

    # - 화면 그리기 구간 ---------------------------#
    drawBoard(screen)
    screen.blit(font_large.render('Tic Tac Toe!', True, (255,255,255)), [40, WINDOW_HEIGHT/2-80])

    # - 화면 그리기 구간 ---------------------------#

    # Performance Debug
    screen.blit(font_small.render(str(round(frameTime/60, 2)), True, (255,255,255)), [10, WINDOW_HEIGHT-20])

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)
    frameTime += 1
    
pygame.quit()