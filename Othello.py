import random

class HumanPlayer():
    def __init__(self,nam,p,o):
        self.name = nam
        self.piece = p
        self.oppo = o

    def move(self,board,legal):
        newboard = list(board)
        counter = ord('a')
        dict = {}
        for i in legal:
            newboard[i] = chr(counter)
            dict[chr(counter)] = i
            counter += 1
        displayBoard(''.join(newboard))
        print()
        counter = ord('a')
        print()
        if len(dict)>0:
            choice = input("What move would you like to make" + ' ('+self.piece+"'s turn) ? ")
            print()
            if choice in dict:
                board = board[0:dict[choice]] + self.piece + board[dict[choice]+1:]
            else:
                choice = input("Try again: ")
                print()
                board = board[0:dict[choice]] + self.piece + board[dict[choice] + 1:]
            positions = turnPieces(self,board,dict[choice],-1)
            positions += turnPieces(self,board,dict[choice], +1)
            positions += turnPieces(self,board,dict[choice], -9)
            positions += turnPieces(self,board,dict[choice], +9)
            positions += turnPieces(self,board,dict[choice], -10)
            positions += turnPieces(self,board,dict[choice], +10)
            positions += turnPieces(self,board,dict[choice], -11)
            positions += turnPieces(self,board,dict[choice], +11)
            for pos in positions:
                board = board[0:pos] + self.piece + board[pos+1:]
        return board

class RandomPlayer():
    def __init__(self,nam,p,o):
        self.name = nam
        self.piece = p
        self.oppo = o

    def move(self,board,legal):
        newboard = list(board)
        counter = ord('a')
        dict = {}
        for i in legal:
            newboard[i] = chr(counter)
            dict[chr(counter)] = i
            counter += 1
        displayBoard(''.join(newboard))
        print()
        counter = ord('a')
        print()
        if len(dict)>0:
            choice = chr(counter+random.randint(0,len(legal)-1))
            board = board[0:dict[choice]] + self.piece + board[dict[choice] + 1:]
            positions = turnPieces(self,board,dict[choice],-1)
            positions += turnPieces(self,board,dict[choice], +1)
            positions += turnPieces(self,board,dict[choice], -9)
            positions += turnPieces(self,board,dict[choice], +9)
            positions += turnPieces(self,board,dict[choice], -10)
            positions += turnPieces(self,board,dict[choice], +10)
            positions += turnPieces(self,board,dict[choice], -11)
            positions += turnPieces(self,board,dict[choice], +11)
            for pos in positions:
                board = board[0:pos] + self.piece + board[pos+1:]
        return board


class MiniMaxPlayer():
    def __init__(self, nam, p, o, b):
        self.name = nam
        self.piece = p
        self.oppo = o
        self.movecount = 0
        self.opponent = ''
        self.neighbors = {}
        self.alphabeta = b

    def setOpponent(self, playeril):
        self.opponent = playeril

    def move(self, board, legal):
        newboard = list(board)
        counter = ord('a')
        dict = {}
        for i in legal:
            newboard[i] = chr(counter)
            dict[chr(counter)] = i
            counter += 1
        displayBoard(''.join(newboard))
        print()
        counter = ord('a')
        print()
        if len(dict) > 0:
            if not self.alphabeta:
                maxe = self.Max_Value(board, 0)
                childs = self.children(board, legal, True)
                theone = 0
                counter = 0
                for child in childs:
                    if self.neighbors[child] >= maxe:
                        board = child
                        theone = legal[counter]
                    counter += 1
                self.movecount += 2
                print(theone)
            else:
                maxe = self.Alpha_Max_Value(board,0,-1000000,1000000)
                childs = self.children(board,legal,True)
                theone = 0
                counter = 0
                for child in childs:
                    if child in self.neighbors:
                        if self.neighbors[child] >= maxe:
                            board = child
                            theone = legal[counter]
                    counter += 1
                self.movecount += 2
                print(theone)
        return board

    def Eval_Func(self, board, movecount):
        # corners 11,81,18,88
        mylen = len(get_legal_moves(self, board))
        theirlen = len(get_legal_moves(self.opponent, board))
        if movecount <= 15:
            weighting = 0
            weighting += .8 * (mylen - theirlen)
            mycount = 0
            theircount = 0
            for i in board:
                if i == self.piece:
                    mycount += 1
                elif i == self.oppo:
                    theircount += 1
            weighting += .2 * (mycount - theircount)
            return weighting
        elif movecount <= 50:
            mycorners = 0
            theircorners = 0
            corners = [11, 18, 81, 88]
            for corner in corners:
                if board[corner] == self.piece:
                    mycorners += 1
                elif board[corner] == self.oppo:
                    theircorners += 1
            return .8*(mycorners - theircorners) + .2*(mylen-theirlen)
        else:
            my = 0
            their = 0
            for i in board:
                if i == self.piece:
                    my += 1
                elif i == self.oppo:
                    their += 1
            return .6*(mylen-theirlen)+.4*(my - their)

    def children(self, board, legal_moves, isAI):
        children = []
        if isAI:
            for move in legal_moves:
                newbo = board[0:move] + self.piece + board[move + 1:]
                positions = turnPieces(self, board, move, -1)
                positions += turnPieces(self, board, move, +1)
                positions += turnPieces(self, board, move, -9)
                positions += turnPieces(self, board, move, +9)
                positions += turnPieces(self, board, move, -10)
                positions += turnPieces(self, board, move, +10)
                positions += turnPieces(self, board, move, -11)
                positions += turnPieces(self, board, move, +11)
                for pos in positions:
                    newbo = newbo[0:pos] + self.piece + newbo[pos + 1:]
                children.append(newbo)
            return children
        else:
            for move in legal_moves:
                newbo = board[0:move] + self.oppo + board[move + 1:]
                positions = turnPieces(self.opponent, board, move, -1)
                positions += turnPieces(self.opponent, board, move, +1)
                positions += turnPieces(self.opponent, board, move, -9)
                positions += turnPieces(self.opponent, board, move, +9)
                positions += turnPieces(self.opponent, board, move, -10)
                positions += turnPieces(self.opponent, board, move, +10)
                positions += turnPieces(self.opponent, board, move, -11)
                positions += turnPieces(self.opponent, board, move, +11)
                for pos in positions:
                    newbo = newbo[0:pos] + self.oppo + newbo[pos + 1:]
                children.append(newbo)
            return children

    def isFinished(self, board):
        if len(get_legal_moves(self, board)) == 0 and len(get_legal_moves(self.opponent, board)) == 0:
            return True
        elif '.' not in board:
            return True
        else:
            mycount = 0
            theircount = 0
            for i in board:
                if i == self.piece:
                    mycount += 1
                elif i == self.oppo:
                    theircount += 1
            if mycount == 0 or theircount == 0:
                return True
        return False

    def Max_Value(self, board, depth):
        if self.isFinished(board) or depth >= 3:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth)
            return self.neighbors[board]
        v = -100000000
        for stat in self.children(board, get_legal_moves(self, board), True):
            v = max(v, self.Min_Value(stat, depth + 1))
        self.neighbors[board] = v
        return v


    def Min_Value(self, board, depth):
        if self.isFinished(board) or depth >= 3:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth)
            return self.neighbors[board]
        v = 100000000
        for stat in self.children(board, get_legal_moves(self.opponent, board), False):
            v = min(v, self.Max_Value(stat, depth + 1))
        self.neighbors[board] = v
        return v

    def Alpha_Max_Value(self, board, depth, alpha, beta):
        if self.isFinished(board) or depth >= 4:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth)
            return self.neighbors[board]
        v = -100000000
        for stat in self.children(board, get_legal_moves(self, board), True):
            v = max(v, self.Alpha_Min_Value(stat, depth + 1,alpha,beta))
            if v > beta: return v
            alpha = max(alpha,v)
        self.neighbors[board] = v
        return v

    def Alpha_Min_Value(self, board, depth, alpha, beta):
        if self.isFinished(board) or depth >= 4:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth)
            return self.neighbors[board]
        v = 100000000
        for stat in self.children(board, get_legal_moves(self.opponent, board), False):
            v = min(v, self.Alpha_Max_Value(stat, depth + 1,alpha,beta))
            if v<alpha: return v
            beta = min(beta,v)
        self.neighbors[board] = v
        return v

def turnPieces(player,board,choice,dir):
    positions = []
    temp = choice + dir
    other = False
    while board[temp] != '.' and board[temp] != '$' and not other:
        if board[temp] == player.piece:
            other = True
        elif board[temp] == player.oppo:
            positions.append(temp)
        temp += dir
    if other:
        return positions
    else:
        return []

def get_legal_moves(player,board):
    legalmoves = []
    for i in range(len(board)):
        if board[i] == '.' and i<=88:
            neighlist = []
            if board[i-1] == player.oppo:
                neighlist.append(i-1)
            if board[i+1] == player.oppo:
                neighlist.append(i+1)
            if board[i-9] == player.oppo:
                neighlist.append(i-9)
            if board[i+9] == player.oppo:
                neighlist.append(i+9)
            if board[i-10] == player.oppo:
                neighlist.append(i-10)
            if board[i+10] == player.oppo:
                neighlist.append(i+10)
            if board[i-11] == player.oppo:
                neighlist.append(i-11)
            if board[i+11] == player.oppo:
                neighlist.append(i+11)
            for neigh in neighlist:
                dir = neigh - i
                temp = neigh
                j = False
                while board[temp] != '$' and board[temp] != '.':
                    if board[temp] == player.piece:
                        legalmoves.append(i)
                        j = True
                        break
                    else:
                        temp += dir
                if j:
                    break
    return legalmoves

def displayBoard(board):
    index = 11
    while index <= 88:
        if index % 10 == 8:
            print(board[index])
            index += 3
        else:
            print(board[index],end=' ')
            index += 1

def initial_board(board):
    boar = ['$'] * 100
    boardcounter = 0
    index = 11
    while boardcounter < len(board):
        boar[index] = board[boardcounter]
        if index % 10 == 8:
            index += 3
        else:
            index += 1
        boardcounter += 1
    return ''.join(boar)

def checkWinner(board,player1,player2):
    if player1.piece not in board:
        return player2.piece + ' wins!'
    elif player2.piece not in board:
        return player1.piece + ' wins!'
    legal1 = get_legal_moves(player1,board)
    legal2 = get_legal_moves(player2,board)
    if len(legal1) == 0 and len(legal2) == 0:
        play1count = 0
        play2count = 0
        for i in board:
            if i == player1.piece:
                play1count += 1
            elif i == player2.piece:
                play2count += 1
        if play1count>play2count:
            return player1.piece + ' wins!'
        elif play2count>play1count:
            return player2.piece + ' wins!'
        else:
            return 'Tie!'
    else:
        return False

# human, random, minimax, alphabeta
one = input('Player 1 is: ')
player1 = ''
if one == 'human':
    player1 = HumanPlayer('Player 1','X','O')
elif one == 'random':
    player1 = RandomPlayer('Player 1','X','O')
elif one == 'minimax':
    player1 = MiniMaxPlayer('Player 1','X','O',False)
elif one == 'alphabeta':
    player1 = MiniMaxPlayer('Player 1','X','O',True)
player2 = ''
two = input('Player 2 is: ')
if two == 'human':
    player2 = HumanPlayer('Player 2','O','X')
elif two == 'random':
    player2 = RandomPlayer('Player 2','O','X')
elif two == 'minimax':
    player2 = MiniMaxPlayer('Player 2', 'O', 'X', False)
elif two == 'alphabeta':
    player2 = MiniMaxPlayer('Player 2', 'O', 'X', True)
if isinstance(player1,MiniMaxPlayer):
    player1.setOpponent(player2)
if isinstance(player2,MiniMaxPlayer):
    player2.setOpponent(player1)
# board = input('Please input the 8by8 board: ')
board = '...........................OX......XO...................................'
theboard = initial_board(board)
turn = 1
while not checkWinner(theboard,player1,player2):
    turn = 1-turn
    if turn == 0:
        legal = get_legal_moves(player1,theboard)
        if len(legal) > 0:
            theboard = player1.move(theboard,legal)
    else:
        legal = get_legal_moves(player2,theboard)
        if len(legal)>0:
            theboard = player2.move(theboard,legal)
displayBoard(theboard)
result = checkWinner(theboard,player1,player2)
print(result)




