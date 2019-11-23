import random
import time

class Strategy():
    # implement all the required methods on your own
    def best_strategy(self, board, player, best_move, running):
        depth = 0
        time.sleep(1)
        while True:
            depth += 1
            best_move.value = self.findMove(board,player,depth)

    def findMove(self,board,player,depth):
        myAI = ''
        count = 0
        for i in board:
            if i == '@' or i == 'o':
                count += 1
        if player == '@':
            myAI = MiniMaxPlayer('Me',player,'o',False,count-4,depth)
        else:
            myAI = MiniMaxPlayer('Me',player,'@',False,count-4,depth)
        legal = get_legal_moves(myAI.piece,myAI.oppo,board)
        maxe = myAI.Max_Value(board,0)
        counter = 0
        for child in myAI.children(board,legal,True):
            if child in myAI.neighbors:
                if myAI.neighbors[child]>=maxe:
                    return legal[counter]
            counter += 1

def turnPieces(thepiece,theirpiece, board, choice, dir):
    positions = []
    temp = choice + dir
    other = False
    while board[temp] != '.' and board[temp] != '?' and not other:
        if board[temp] == thepiece:
            other = True
        elif board[temp] == theirpiece:
            positions.append(temp)
        temp += dir
    if other:
        return positions
    else:
        return []

def get_legal_moves(thepiece,theirpiece, board):
    legalmoves = []
    for i in range(len(board)):
        if board[i] == '.' and i <= 88:
            neighlist = []
            if board[i - 1] == theirpiece:
                neighlist.append(i - 1)
            if board[i + 1] == theirpiece:
                neighlist.append(i + 1)
            if board[i - 9] == theirpiece:
                neighlist.append(i - 9)
            if board[i + 9] == theirpiece:
                neighlist.append(i + 9)
            if board[i - 10] == theirpiece:
                neighlist.append(i - 10)
            if board[i + 10] == theirpiece:
                neighlist.append(i + 10)
            if board[i - 11] == theirpiece:
                neighlist.append(i - 11)
            if board[i + 11] == theirpiece:
                neighlist.append(i + 11)
            for neigh in neighlist:
                dir = neigh - i
                temp = neigh
                j = False
                while board[temp] != '?' and board[temp] != '.':
                    if board[temp] == thepiece:
                        legalmoves.append(i)
                        j = True
                        break
                    else:
                        temp += dir
                if j:
                    break
    return legalmoves

class MiniMaxPlayer():
    def __init__(self, nam, p, o, b, mo,d):
        self.name = nam
        self.piece = p
        self.oppo = o
        self.movecount = mo
        self.depth = d
        self.opponent = ''
        self.neighbors = {}
        self.alphabeta = b

    def Eval_Func(self, board, movecount, whosemove):
        # corners 11,81,18,88
        mymoves = get_legal_moves(self.piece,self.oppo, board)
        theirmoves = get_legal_moves(self.oppo,self.piece, board)
        mylen = len(mymoves)
        theirlen = len(theirmoves)
        mycount = 0
        theircount = 0
        mypieces = []
        theirpieces = []
        counter = 0
        for i in board:
            if i == self.piece:
                mycount += 1
                mypieces.append(counter)
            elif i == self.oppo:
                theircount += 1
                theirpieces.append(counter)
            counter += 1
        mycorners = 0
        theircorners = 0
        corners = [11, 18, 81, 88]
        for corner in corners:
            if board[corner] == self.piece:
                mycorners += 1
            elif board[corner] == self.oppo:
                theircorners += 1
        mystable = 0
        theirstable = 0
        mynextmoves = children(board,mymoves,True)
        theirnextmoves = children(board,theirmoves,False)
            
        # coinheu = 0
        # mobiheu = 0
        # cornerheu = 0
        # coinheu = 100 * (mycount-theircount)/(mycount+theircount)
        # if (mylen+theirlen) != 0:
        #     mobiheu = 100 * (mylen-theirlen)/(mylen+theirlen)
        # if (mycorners+theircorners) != 0:
        #     cornerheu = 100 * (mycorners-theircorners) / (mycorners+theircorners)
        # return 30 * (cornerheu) + 15 * (mobiheu) + 5 * (coinheu)
        if movecount <= 15:
            weighting = 0
            weighting += .8 * (mylen - theirlen)
            weighting += .2 * (mycount - theircount)
            return weighting
        elif movecount <= 50:
            return .9*(mycorners - theircorners) + .1*(mylen-theirlen)
        else:
            return .4*(mylen-theirlen)+.6*(mycount - theircount)

    def children(self, board, legal_moves, isAI):
        children = []
        if isAI:
            for move in legal_moves:
                newbo = board[0:move] + self.piece + board[move + 1:]
                positions = turnPieces(self.piece, self.oppo, board, move, -1)
                positions += turnPieces(self.piece, self.oppo, board, move, +1)
                positions += turnPieces(self.piece, self.oppo, board, move, -9)
                positions += turnPieces(self.piece, self.oppo, board, move, +9)
                positions += turnPieces(self.piece, self.oppo, board, move, -10)
                positions += turnPieces(self.piece, self.oppo, board, move, +10)
                positions += turnPieces(self.piece, self.oppo, board, move, -11)
                positions += turnPieces(self.piece, self.oppo, board, move, +11)
                for pos in positions:
                    newbo = newbo[0:pos] + self.piece + newbo[pos + 1:]
                children.append(newbo)
            return children
        else:
            for move in legal_moves:
                newbo = board[0:move] + self.oppo + board[move + 1:]
                positions = turnPieces(self.oppo,self.piece, board, move, -1)
                positions += turnPieces(self.oppo,self.piece, board, move, +1)
                positions += turnPieces(self.oppo,self.piece, board, move, -9)
                positions += turnPieces(self.oppo,self.piece, board, move, +9)
                positions += turnPieces(self.oppo,self.piece, board, move, -10)
                positions += turnPieces(self.oppo,self.piece, board, move, +10)
                positions += turnPieces(self.oppo,self.piece, board, move, -11)
                positions += turnPieces(self.oppo,self.piece, board, move, +11)
                for pos in positions:
                    newbo = newbo[0:pos] + self.oppo + newbo[pos + 1:]
                children.append(newbo)
            return children

    def isFinished(self, board):
        if len(get_legal_moves(self.piece,self.oppo, board)) == 0 and len(get_legal_moves(self.oppo,self.piece, board)) == 0:
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
        if self.isFinished(board) or depth >= self.depth:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth, 1)
            return self.neighbors[board]
        v = -100000000
        for stat in self.children(board, get_legal_moves(self.piece,self.oppo, board), True):
            v = max(v, self.Min_Value(stat, depth + 1))
        self.neighbors[board] = v
        return v


    def Min_Value(self, board, depth):
        if self.isFinished(board) or depth >= self.depth:
            self.neighbors[board] = self.Eval_Func(board, self.movecount + depth, -1)
            return self.neighbors[board]
        v = 100000000
        for stat in self.children(board, get_legal_moves(self.oppo,self.piece, board), False):
            v = min(v, self.Max_Value(stat, depth + 1))
        self.neighbors[board] = v
        return v
