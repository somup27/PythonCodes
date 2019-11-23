from collections import deque
import copy
import sys
import random

def revCheck(board):
    revboard = [board[len(board)-1-x][::-1] for x in range(len(board))]
    return board == revboard

def ConnectionCheck(board,openchars):
    openpos = (0,0)
    found = False
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '-':
                openpos = (i,j)
                found = True
                break
        if found:
            break
    component = ConnectionHelper(board,openpos)
    return component == openchars

def ConnectionHelper(board,pos):
    frontier = deque()
    frontier.appendleft(pos)
    explored = set()
    explored.add(pos)
    count = 1
    while frontier:
        node = frontier.popleft()
        left = (node[0],node[1]-1)
        up = (node[0]-1,node[0])
        right = (node[0],node[1]+1)
        down = (node[0]+1,node[1])
        if inBounds(board,left) and (board[left[0]][left[1]] == '~' or board[left[0]][left[1]] == '-') and left not in explored:
            explored.add(left)
            frontier.append(left)
            count += 1
        if inBounds(board,up) and (board[up[0]][up[1]] == '~' or board[up[0]][up[1]] == '-') and up not in explored:
            explored.add(up)
            frontier.append(up)
            count += 1
        if inBounds(board,right) and (board[right[0]][right[1]] == '~' or board[right[0]][right[1]] == '-') and right not in explored:
            explored.add(right)
            frontier.append(right)
            count += 1
        if inBounds(board,down) and (board[down[0]][down[1]] == '~' or board[down[0]][down[1]] == '-') and down not in explored:
            explored.add(down)
            frontier.append(down)
            count += 1
    return count


def inBounds(board, pos):
    return pos[0] >= 0 and pos[0] < len(board) and pos[1] >= 0 and pos[1] < len(board[0])

def displayBoard(board):
    for i in board:
        for char in i:
            print(char,end='')
        print()

def force_blocks(board):
    newerblocks = set()
    boo = False
    for i in range(len(board)):
        for j in range(len(board[0])):
            currpos = (i, j)
            onerpos = (i, j + 1)
            tworpos = (i, j + 2)
            threerpos = (i, j + 3)
            onedpos = (i + 1, j)
            twodpos = (i + 2, j)
            threedpos = (i + 3, j)
            if board[currpos[0]][currpos[1]] == '#':
                if inBounds(board, tworpos) and board[tworpos[0]][tworpos[1]] == '#' and inBounds(board, onerpos) and board[onerpos[0]][onerpos[1]] == '-':
                    newerblocks.add(onerpos)
                    boo = True
                elif inBounds(board, threerpos) and board[threerpos[0]][threerpos[1]] == '#' and inBounds(board,onerpos) and board[onerpos[0]][onerpos[1]] == '-' and inBounds(board, tworpos) and board[tworpos[0]][tworpos[1]] == '-':
                    newerblocks.add(onerpos)
                    newerblocks.add(tworpos)
                    boo = True
                elif inBounds(board, onerpos) and board[onerpos[0]][onerpos[1]] == '-' and onerpos[1] == len(board[0]) - 1:
                    newerblocks.add(onerpos)
                    boo = True
                elif inBounds(board, onerpos) and board[onerpos[0]][onerpos[1]] == '-' and inBounds(board, tworpos) and board[tworpos[0]][tworpos[1]] == '-' and tworpos[1] == len(board[0]) - 1:
                    newerblocks.add(onerpos)
                    newerblocks.add(tworpos)
                    boo = True
            elif currpos[1] == 0 and board[currpos[0]][currpos[1]] == '-':
                if inBounds(board, onerpos) and board[onerpos[0]][onerpos[1]] == '#':
                    newerblocks.add(currpos)
                    boo = True
                elif inBounds(board, tworpos) and board[tworpos[0]][tworpos[1]] == '#' and inBounds(board, onerpos) and board[onerpos[0]][onerpos[1]] == '-':
                    newerblocks.add(onerpos)
                    newerblocks.add(currpos)
                    boo = True
            if board[currpos[0]][currpos[1]] == '#':
                if inBounds(board, twodpos) and board[twodpos[0]][twodpos[1]] == '#' and inBounds(board, onedpos) and board[onedpos[0]][onedpos[1]] == '-':
                    newerblocks.add(onedpos)
                    boo = True
                elif inBounds(board, threedpos) and board[threedpos[0]][threedpos[1]] == '#' and inBounds(board,onedpos) and board[onedpos[0]][onedpos[1]] == '-' and inBounds(board, twodpos) and board[twodpos[0]][
                    twodpos[1]] == '-':
                    newerblocks.add(onedpos)
                    newerblocks.add(twodpos)
                    boo = True
                elif inBounds(board, onedpos) and board[onedpos[0]][onedpos[1]] == '-' and onedpos[0] == len(board) - 1:
                    newerblocks.add(onedpos)
                    boo = True
                elif inBounds(board, onedpos) and board[onedpos[0]][onedpos[1]] == '-' and inBounds(board, twodpos) and board[twodpos[0]][twodpos[1]] == '-' and twodpos[0] == len(board) - 1:
                    newerblocks.add(onedpos)
                    newerblocks.add(twodpos)
                    boo = True
            elif currpos[0] == 0 and board[currpos[0]][currpos[1]] == '-':
                if inBounds(board, onedpos) and board[onedpos[0]][onedpos[1]] == '#':
                    newerblocks.add(currpos)
                    boo = True
                elif inBounds(board, twodpos) and board[twodpos[0]][twodpos[1]] == '#' and inBounds(board, onedpos) and board[onedpos[0]][onedpos[1]] == '-':
                    newerblocks.add(onedpos)
                    newerblocks.add(currpos)
                    boo = True
    for pos in newerblocks:
        board[pos[0]][pos[1]] = '#'
    return board, newerblocks, boo

# def force_protected(board):
#     newerprocs = set()
#     boo = False
#     for i in range(len(board)):
#         for j in range(len(board[0])):
#             if j+3 < len(board[0]):
#                 ch = ''.join([board[i][k] for k in range(j,j+4)])
#                 if ch == '#-~-':
#                     newerprocs.add((i,j+3))
#                     boo = True
#                 elif ch == '#~--':
#                     newerprocs.add((i,j+2))
#                     newerprocs.add((i,j+3))
#                     boo = True
#     for proc in newerprocs:
#         board[proc[0]][proc[1]] = '~'
#     return board,newerprocs,boo

def place_blocks(board, blockcount, blocks, openc):
    boo = True
    x = len(board)-1
    y = len(board[0])-1
    for i in range(len(board)):
        for j in range(len(board[0])):
            x1 = x-i
            y1 = y-j
            if board[i][j] == '#' and board[x1][y1] == '-':
                board[x1][y1] = '#'
                blockcount += 1
                openc -= 1
            elif board[i][j] == '-' and board[x1][y1] == '#':
                board[i][j] = '#'
                blockcount += 1
                openc -= 1
            elif board[i][j] == '~' and board[x1][y1] == '-':
                board[x1][y1] = '~'
                openc -= 1
            elif board[i][j] == '-' and board[x1][y1] == '~':
                board[i][j] = '~'
                openc -= 1
    while boo:
        theboard, newblocks, checker = force_blocks(board)
        blockcount += len(newblocks)
        openc -= len(newblocks)
        boo = checker
        board = theboard
        displayBoard(board)
        print()
    # boo = True
    # while boo:
    #     theboard, newprocs, checker = force_protected(board)
    #     openc -= len(newprocs)
    #     boo = checker
    #     board = theboard
    #     displayBoard(board)
    #     print()
    displayBoard(theboard)
    print()
    isBoard = False
    revert = copy.deepcopy(board)
    oricount = blockcount
    orichar = openc
    while not isBoard:
        while blockcount < blocks:
            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board[0])-1)
            x1 = len(board)-1-x
            y1 = len(board[0])-1-y
            if board[x][y] == '-':
                up1 = (x-1,y)
                up2 = (x-2,y)
                down1 = (x+1,y)
                down2 = (x+2,y)
                left1 = (x,y-1)
                left2 = (x,y-2)
                right1 = (x,y+1)
                right2 = (x,y+2)
                if ((inBounds(board,up1) and board[up1[0]][up1[1]] != '~') or not inBounds(board,up1)) and ((inBounds(board,up2) and board[up2[0]][up2[1]] != '~') or not inBounds(board,up2)) and ((inBounds(board,down1) and board[down1[0]][down1[1]] != '~') or not inBounds(board,down1)) and ((inBounds(board,down2) and board[down2[0]][down2[1]] != '~') or not inBounds(board,down2)) and ((inBounds(board,left1) and board[left1[0]][left1[1]] != '~') or not inBounds(board,left1)) and ((inBounds(board,left2) and board[left2[0]][left2[1]] != '~') or not inBounds(board,left2)) and ((inBounds(board,right1) and board[right1[0]][right1[1]] != '~') or not inBounds(board,right2)) and ((inBounds(board,right2) and board[right2[0]][right2[1]] != '~') or not inBounds(board,right2)):
                    board[x][y] ='#'
                    blockcount += 1
                    openc -= 1
                    if board[x1][y1] == '-':
                        board[x1][y1] = '#'
                        blockcount += 1
                        openc -= 1
            elif board[x][y] == '#':
                if board[x1][y1] == '-':
                    board[x1][y1] = '#'
                    blockcount += 1
                    openc -= 1
            neuboard, bocc, bo = force_blocks(board)
            board = neuboard
            blockcount += len(bocc)
            openc -= len(bocc)
            # neuboard, pocc, po = force_protected(board)
            # board = neuboard
            # openc -= len(pocc)
        neuboard, bocc, bo = force_blocks(board)
        board = neuboard
        blockcount += len(bocc)
        openc -= len(bocc)
        # neuboard, pocc, po = force_protected(board)
        # board = neuboard
        # openc -= len(pocc)
        tild = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == '~':
                    tild += 1
        if blockcount == blocks:
            displayBoard(board)
            print()
        if blockcount == blocks and ConnectionCheck(board,openc+tild):
            isBoard = True
        else:
            board = copy.deepcopy(revert)
            blockcount = oricount
            openc = orichar
    return board

args = sys.argv[1:]
h,w = [int(x) for x in args[0].split('x')]
opencount = h*w
theboard = [['-' for x in range(w)] for i in range(h)]
blocks = int(args[1])
blockcount = 0
setting = args[3:]
placements = {}
for i in setting:
    orientation = i[0]
    fpos = ''
    spos = ''
    ind = 1
    foundX = False
    while True:
        if i[ind] == 'x' and foundX == False:
            foundX = True
            ind += 1
        elif i[ind].isdigit() and foundX:
            spos += i[ind]
            ind += 1
        elif i[ind].isdigit():
            fpos += i[ind]
            ind += 1
        else:
            break
    fpos,spos = int(fpos),int(spos)
    chars = i[ind:]
    temp = (fpos,spos)
    if orientation == 'H':
        charcounter = 0
        while charcounter < len(chars):
            if chars[charcounter] == '#':
                if theboard[temp[0]][temp[1]] != '#':
                    blockcount += 1
                    theboard[temp[0]][temp[1]] = '#'
            else:
                if theboard[temp[0]][temp[1]] != '~':
                    theboard[temp[0]][temp[1]] = '~'
                    if chars[charcounter] in placements:
                        placements[chars[charcounter]].append(temp)
                    else:
                        placements[chars[charcounter]] = [temp]
                    opencount -= 1
            temp = (temp[0],temp[1]+1)
            charcounter += 1
    else:
        charcounter = 0
        while charcounter < len(chars):
            if chars[charcounter] == '#':
                if theboard[temp[0]][temp[1]] != '#':
                    blockcount += 1
                    theboard[temp[0]][temp[1]] = '#'
            else:
                if theboard[temp[0]][temp[1]] != '~':
                    theboard[temp[0]][temp[1]] = '~'
                    if chars[charcounter] in placements:
                        placements[chars[charcounter]].append(temp)
                    else:
                        placements[chars[charcounter]] = [temp]
                    opencount -= 1
            temp = (temp[0]+1,temp[1])
            charcounter += 1
displayBoard(theboard)
print()
if blocks == opencount:
    displayBoard(['#' for i in range(w)] for j in range(h))
elif blocks == 0 or blockcount == blocks:
    for char in placements:
        for pos in placements[char]:
            theboard[pos[0]][pos[1]] = char
    for i in range(len(theboard)):
        for j in range(len(theboard[0])):
            if theboard[i][j] == '~':
                theboard[i][j] = '-'
    displayBoard(theboard)
else:
    theboard = place_blocks(theboard, blockcount, blocks, opencount-blockcount)
    for char in placements:
        for pos in placements[char]:
            theboard[pos[0]][pos[1]] = char
    for i in range(len(theboard)):
        for j in range(len(theboard[0])):
            if theboard[i][j] == '~':
                theboard[i][j] = '-'
    displayBoard(theboard)