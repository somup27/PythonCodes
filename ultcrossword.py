import sys
import random

def displayBoard(board):
    for i in board:
        for char in i:
            print(char, end='')
        print()


def ConnectionCheck(board):
    openpos = (0, 0)
    found = False
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '-':
                openpos = (i, j)
                found = True
                break
        if found:
            break
    component = ConnectionHelper(board, openpos)
    for i in range(len(component)):
        for j in range(len(component[0])):
            if component[i][j] != '#':
                return False
    return True


def ConnectionHelper(board, pos):
    if not inBounds(board, pos): return board
    if board[pos[0]][pos[1]] == '-' or board[pos[0]][pos[1]] == '~':
        board[pos[0]][pos[1]] = '#'
        board = ConnectionHelper(board, (pos[0], pos[1] - 1))
        board = ConnectionHelper(board, (pos[0], pos[1] + 1))
        board = ConnectionHelper(board, (pos[0] - 1, pos[1]))
        board = ConnectionHelper(board, (pos[0] + 1, pos[1]))
    return board


def inBounds(board, pos):
    return pos[0] >= 0 and pos[0] < len(board) and pos[1] >= 0 and pos[1] < len(board[0])


def border(board):
    board.insert(0, ['#' for i in range(len(board[0]) + 2)])
    board.append(['#' for i in range(len(board[0]))])
    for i in range(len(board)):
        if i != 0 and i != len(board) - 1:
            board[i].insert(0, '#')
            board[i].append('#')
    return board


def removeBorder(board):
    board.pop(0)
    board.pop(len(board) - 1)
    for i in range(len(board)):
        board[i].pop(0)
        board[i].pop(len(board[i]) - 1)
    return board


def force_blocks(board, openchars):
    count = 0
    for i in range(len(board) - 1):
        for j in range(len(board[0])):
            if j + 2 < len(board[0]):
                if ''.join([board[i][k] for k in range(j, j + 3)]) == '#-#':
                    board[i][j + 1] = '#'
                    openchars.remove((i, j + 1))
                    count += 1
                elif j + 3 < len(board[0]):
                    if ''.join([board[i][k] for k in range(j, j + 4)]) == '#--#':
                        board[i][j + 1] = '#'
                        board[i][j + 2] = '#'
                        openchars.remove((i, j + 1))
                        openchars.remove((i, j + 2))
                        count += 2
            if i + 2 < len(board):
                if ''.join([board[k][j] for k in range(i, i + 3)]) == '#-#':
                    board[i + 1][j] = '#'
                    openchars.remove((i + 1, j))
                    count += 1
                elif i + 3 < len(board):
                    if ''.join([board[k][j] for k in range(i, i + 4)]) == '#--#':
                        board[i + 1][j] = '#'
                        board[i + 2][j] = '#'
                        openchars.remove((i + 1, j))
                        openchars.remove((i + 2, j))
                        count += 2
    return board, count, openchars


def lenCheck(board):
    for i in range(len(board) - 1):
        for j in range(len(board[0])):
            if j + 2 < len(board[0]):
                checke = board[i][j] + board[i][j + 1] + board[i][j + 2]
                if checke == '#-#' or checke == '#~#':
                    return False
                elif j + 3 < len(board[0]):
                    checke = board[i][j] + board[i][j + 1] + board[i][j + 2] + board[i][j + 3]
                    if checke == '#--#' or checke == '#~-#' or checke == '#-~#' or checke == '#~~#':
                        return False
            if i + 2 < len(board):
                checke = board[i][j] + board[i + 1][j] + board[i + 2][j]
                if checke == '#-#' or checke == '#~#':
                    return False
                elif i + 3 < len(board):
                    checke = board[i][j] + board[i + 1][j] + board[i + 2][j] + board[i + 3][j]
                    if checke == '#--#' or checke == '#~-#' or checke == '#-~#' or checke == '#~~#':
                        return False
    return True


def place_blocks(board, blockcount, blocks, openc, openchars):
    if len(board) % 2 == 1 and len(board[0]) % 2 == 1 and blocks % 2 == 1 and board[int((1 + len(board) - 2) / 2)][
        int((1 + len(board[0]) - 2) / 2)] == '-':
        board[int((1 + len(board) - 2) / 2)][int((1 + len(board[0]) - 2) / 2)] = '#'
        openchars.remove(((int(1 + len(board) - 2) / 2), int((1 + len(board[0]) - 2) / 2)))
        openc -= 1
        blockcount += 1
    neuboard, blocked, open = force_blocks(board, openchars)
    blockcount += blocked
    openc -= blocked
    board = neuboard
    displayBoard(board)
    openchars = open
    print()
    x = len(board) - 1
    y = len(board[0]) - 1
    for i in range(1, len(board) - 1):
        for j in range(1, len(board[0]) - 1):
            x1 = x - i
            y1 = y - j
            if board[i][j] == '#' and board[x1][y1] == '-':
                board[x1][y1] = '#'
                blockcount += 1
                openchars.remove((x1, y1))
                openc -= 1
            elif board[i][j] == '-' and board[x1][y1] == '#':
                board[i][j] = '#'
                blockcount += 1
                openchars.remove((i, j))
                openc -= 1
            elif board[i][j] == '~' and board[x1][y1] == '-':
                board[x1][y1] = '~'
                openchars.remove((x1, y1))
                openc -= 1
            elif board[i][j] == '-' and board[x1][y1] == '~':
                board[i][j] = '~'
                openchars.remove((i, j))
                openc -= 1
    displayBoard(board)
    print()
    oriboard = list([list(i) for i in board])
    oriblock = blockcount
    orichar = openc
    orichars = list(openchars)
    isBoard = False
    while not isBoard:
        while blockcount < blocks:
            x, y = openchars[random.randint(0, len(openchars) - 1)]
            x1 = len(board) - 1 - x
            y1 = len(board[0]) - 1 - y
            if board[x][y] == '-' and board[x1][y1] == '-':
                if x != x1 or y != y1:
                    board[x][y] = '#'
                    board[x1][y1] = '#'
                    openchars.remove((x, y))
                    openchars.remove((x1, y1))
                    openc -= 2
                    blockcount += 2
                else:
                    board[x][y] = '#'
                    openchars.remove((x, y))
                    openc -= 1
                    blockcount += 1
            neuboard, count, open = force_blocks(board, openchars)
            blockcount += count
            openc -= count
            board = neuboard
            openchars = open
        neuboard, count, open = force_blocks(board, openchars)
        blockcount += count
        openc -= count
        board = neuboard
        openchars = open
        realblock = 0
        for i in range(1, len(board) - 1):
            for j in range(1, len(board[0]) - 1):
                if board[i][j] == '#':
                    realblock += 1
        if realblock == blocks:
            displayBoard(board)
            print()
        if realblock == blocks and ConnectionCheck(list([list(i) for i in board])) and lenCheck(board):
            displayBoard(board)
            print()
            isBoard = True
        else:
            board = list([list(i) for i in oriboard])
            openc = orichar
            blockcount = oriblock
            openchars = list(orichars)
    return board


def generateBoard(args):
    h, w = [int(x) for x in args[0].split('x')]
    opencount = h * w
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
        fpos, spos = int(fpos), int(spos)
        chars = i[ind:]
        temp = (fpos, spos)
        if orientation == 'H' or orientation == 'h':
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
                            placements[chars[charcounter].lower()].append(temp)
                        else:
                            placements[chars[charcounter].lower()] = [temp]
                        opencount -= 1
                temp = (temp[0], temp[1] + 1)
                charcounter += 1
        elif orientation == 'V' or orientation == 'v':
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
                            placements[chars[charcounter].lower()].append(temp)
                        else:
                            placements[chars[charcounter].lower()] = [temp]
                        opencount -= 1
                temp = (temp[0] + 1, temp[1])
                charcounter += 1
    if blocks == opencount:
        theboard = [['#' for i in range(w)] for j in range(h)]
        displayBoard(theboard)
        print()
        return theboard
    elif blocks == 0 or blockcount == blocks:
        for char in placements:
            for pos in placements[char]:
                theboard[pos[0]][pos[1]] = char
        for i in range(len(theboard)):
            for j in range(len(theboard[0])):
                if theboard[i][j] == '~':
                    theboard[i][j] = '-'
        displayBoard(theboard)
        print()
        return theboard
    else:
        theboard = border(theboard)
        displayBoard(theboard)
        print()
        openchars = []
        for i in range(1, len(theboard) - 1):
            for j in range(1, len(theboard[0]) - 1):
                if theboard[i][j] == '-':
                    openchars.append((i, j))
        theboard = place_blocks(theboard, blockcount, blocks, opencount - blockcount, openchars)
        theboard = removeBorder(theboard)
        for char in placements:
            for pos in placements[char]:
                theboard[pos[0]][pos[1]] = char
        for i in range(len(theboard)):
            for j in range(len(theboard[0])):
                if theboard[i][j] == '~':
                    theboard[i][j] = '-'
        displayBoard(theboard)
        print()
        return theboard


def match(word, dic):
    bou = True
    for i in word[len(word)-1]:
        if i != '-':
            bou = False
            break
    if bou:
        return dic[len(word[len(word)-1])]
    else:
        pos_words = dic[len(word[len(word)-1])]
        checker = word[len(word)-1]
        wori = []
        for i in pos_words:
            boo = True
            for j in range(len(checker)):
                if checker[j] != '-':
                    if checker[j] != i[j]:
                        boo = False
                        break
            if boo:
                wori.append(i)
        return wori


# def recursive_backtracking(assignment,variables,neighbors):
#     if check_complete(assignment): return assignment
#     var = select_var(assignment,variables,neighbors)
#     for val in variables[var]:
#         if isValid(val,var,assignment,neighbors):
#             assignment[var] = val
#             prevvals = list(variables[var])
#             variables,ne = update(val,var,variables,neighbors)
#             result = recursive_backtracking(assignment,variables,neighbors)
#             if result != None: return result
#             del assignment[var]
#             variables[var] = prevvals
#             for neighbor in ne:
#                 variables[neighbor].append(val)
#     return None
#

def check_match(filling,mat):
    for i in range(len(filling)):
        if filling[i] != '-':
            if filling[i] != mat[i]:
                return False
    return True

def findWordIndex(filling):
    for i in range(len(filling)):
        if isinstance(filling[i],str):
            return i

def backtracking_search(words, completed, dic,explored,regdic):
    if len(words) == 0: return completed
    words.sort()
    filling = words.pop(0)
    fillingcopy = list(filling)
    wordscopy = [list(word) for word in words]
    completedcopy = [list(complete) for complete in completed]
    exploredcopy = set(explored)
    regdiccopy = dict(regdic)
    wo = findWordIndex(filling)
    matches = filling[wo+1:]
    for mat in matches:
        if mat not in explored and check_match(filling[wo],mat):
            changedpos = []
            for i in range(len(filling[wo])):
                if filling[wo][i] == '-':
                    changedpos.append((filling[i+1], mat[i]))
            filling[wo] = mat
            filling[0] = 0
            completed.append(filling)
            explored.add(mat)
            res = update(changedpos, words, completed,explored,dic,regdic)
            if res != False:
                result = backtracking_search(res[0], res[1], dic,res[2],res[3])
                if result != None: return result
            words = [list(word) for word in wordscopy]
            completed = [list(complete) for complete in completedcopy]
            explored = set(exploredcopy)
            filling = list(fillingcopy)
            regdic = dict(regdiccopy)
    return None

def update(changes,words,completed,explored,dic,regdic):
    boo = False
    while True:
        for i in range(len(words)):
            chec = words[i]
            wo = findWordIndex(chec)
            for change in changes:
                if change[0] in chec:
                    lo = chec.index(change[0]) - 1
                    chec[wo] = chec[wo][0:lo] + change[1] + chec[wo][lo+1:]
                    if chec[wo] in regdic:
                        chec = chec[0:wo+1] + regdic[chec[wo]]
                        chec[0] = len(regdic[chec[wo]])
                    else:
                        maty = []
                        for mat in chec[wo+1:]:
                            if check_match(chec[wo],mat):
                                maty.append(mat)
                        regdic[chec[wo]] = maty
                        chec = chec[0:wo+1] + maty
                        chec[0] = len(maty)
                    words[i] = chec
            if '-' not in words[i][wo]:
                che = words.pop(i)
                if che[wo] not in dic[len(che[wo])]:
                    return False
                explored.add(che[wo])
                completed.append(che)
                boo = True
                break
        if not boo:
            break
        boo = False
    return [words,completed,explored,regdic]

args = sys.argv[1:]
board = generateBoard(args)
hwords = []
vwords = []
for i in range(len(board)):
    j = 0
    temp = ''
    temppos = []
    tempdash = 0
    while j < len(board[0]):
        if board[i][j] == '#':
            if temp != '':
                hwords.append([tempdash]+temppos + [temp])
                temp = ''
                temppos = []
                tempdash = 0
        else:
            if board[i][j] == '-':
                tempdash += 1
            temp += board[i][j]
            temppos.append((i, j))
        j += 1
    if temp != '':
        hwords.append([tempdash]+temppos + [temp])
for i in range(len(board[0])):
    j = 0
    temp = ''
    temppos = []
    tempdash = 0
    while j < len(board):
        if board[j][i] == '#':
            if temp != '':
                vwords.append([tempdash]+temppos + [temp])
                temp = ''
                temppos = []
                tempdash = 0
        else:
            if board[j][i] == '-':
                tempdash += 1
            temp += board[j][i]
            temppos.append((j, i))
        j += 1
    if temp != '':
        vwords.append([tempdash]+temppos + [temp])
dic = {}
words = open(args[2], 'r')
words = words.readlines()
for word in words:
    word = word.replace('\n', '')
    if len(word) in dic:
        dic[len(word)].append(word)
    else:
        dic[len(word)] = [word]
ultwords = hwords + vwords
regdic = {}
for p in range(len(ultwords)):
    wor = ultwords[p][len(ultwords[p])-1]
    if wor not in regdic:
        matc = match(ultwords[p],dic)
        regdic[wor] = matc
        ultwords[p] += matc
        ultwords[p][0] = len(matc)
    else:
        ultwords[p] += regdic[wor]
        ultwords[p][0] = len(regdic[wor])
completes = backtracking_search(ultwords,[],dic,set(),regdic)
finalboard = board
for word in completes:
    wo = findWordIndex(word)
    for ind in range(1,wo):
        finalboard[word[ind][0]][word[ind][1]] = word[wo][ind-1]
displayBoard(finalboard)

