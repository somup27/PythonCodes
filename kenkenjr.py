import copy

def recursiveBacktracking(rows,columns,sections,assignment,lookup1,lookup2):
    if completion(assignment): return assignment # If the puzzle is complete return the assignment
    i = selectvar(assignment) # Returns the first square that isn't filled in
    for j in range(1,4): # All possible values that can fit in a box
        if isValid(rows,columns,sections,lookup1,lookup2,i,j): # Checking if the given value can fill the given box
            assignment[i] = j # Assigning the index with the value
            t, y, e = lookup1[i] # What row, column , square the index is in
            pos1, pos2, pos3 = lookup2[i] # what the position of index in the row, column, square
            rowers = rows.copy()
            cols = columns.copy()
            sq = copy.deepcopy(sections) # Making copies  of the rows, cols, squares
            row = list(rowers[t])
            column = list(cols[y])
            section = list(sq[e][0])
            row[pos1] = str(j)
            column[pos2] = str(j)
            section[pos3] = str(j)
            row = "".join(row)
            column = "".join(column)
            section = "".join(section)
            rowers[t] = row
            cols[y] = column
            sq[e][0] = section # Update the rows, cols, squares affected by the change
            result = recursiveBacktracking(rowers,cols,sq,assignment,lookup1,lookup2) # Recursive call
            if result != None: return result # return assignment if its complete
            del assignment[i] # delete if the function backtracks
    return None

def selectvar(assignment): # Looking for the first box that is unfilled
    for i in range(9):
        if i not in assignment:
            return i

def completion(assignment):
    for i in range(9):
        if i not in assignment: # Checking if every single box is filled
            return False
    return True

def isValid(rows,columns,sections,lookup1,lookup2,var,val):
    row,column,section = lookup1[var] # What row, column , square the index is in
    pos1,pos2,pos3 = lookup2[var] # what the position of index in the row, column, square
    val = str(val)
    row = rows[row]
    column = columns[column]
    section = sections[section]
    if row[pos1] == "-" and column[pos2] == "-" and section[0][pos3] == "-": # Checking if the box is empty
        if val not in row and val not in column:
            yu = list(section[0])
            yu[pos3] = val
            if '-' not in yu:
                if sum([int(y) for y in yu]) == section[1]:
                    return True
                return False
            return True
        return False
    return False

lookup1 = {}
lookup2 = {}
beginboard = ['-' for i in range(9)]
inplist = input().split(', ')
anslist = input().split(', ')
for i in range(len(inplist)-1):
    if '#' in inplist[i+1]:
        beginboard[int(inplist[i])-1] = inplist[i+1][0]
beginboard = ''.join(beginboard)
rows = [beginboard[0:3],beginboard[3:6],beginboard[6:9]]
columns = [beginboard[0::3],beginboard[1::3],beginboard[2::3]]
sections = []
for i in range(9):
    lookup1[i] = [i//3,i%3]
    lookup2[i] = [i%3,i//3]
sectioncount = 0
for h in range(1,len(inplist)):
    # if '+' in inplist[h+2]:
    if '+' in inplist[h]:
        if h-3 > 0 and '+' not in inplist[h-3] and '#' not in inplist[h-3]:
            tempsection = ''
            first = int(inplist[h-3]) - 1
            second = int(inplist[h-2]) - 1
            third = int(inplist[h-1])-1
            tempsection += beginboard[first]
            tempsection += beginboard[second]
            tempsection += beginboard[third]
            lookup1[first].append(sectioncount)
            lookup1[second].append(sectioncount)
            lookup1[third].append(sectioncount)
            lookup2[first].append(0)
            lookup2[second].append(1)
            lookup2[third].append(2)
            sections.append([tempsection, int(inplist[h][0])])
            sectioncount += 1
        else:
            tempsection = ''
            first = int(inplist[h-2]) - 1
            second = int(inplist[h-1]) - 1
            tempsection += beginboard[first]
            tempsection += beginboard[second]
            lookup1[first].append(sectioncount)
            lookup1[second].append(sectioncount)
            lookup2[first].append(0)
            lookup2[second].append(1)
            sections.append([tempsection, int(inplist[h][0])])
            sectioncount += 1
assignment = {}
for i in range(9):
    if beginboard[i] != '-':
        assignment[i] = int(beginboard[i])
solution = recursiveBacktracking(rows,columns,sections,assignment,lookup1,lookup2)
for ans in anslist:
    print(solution[int(ans)-1])





