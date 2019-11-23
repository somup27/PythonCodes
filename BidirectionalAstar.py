# Name: Somu Patil        Date: 10/5/18
import math, random, time, heapq


class PriorityQueue():
    """Implementation of a priority queue
    to store nodes during search."""

    # TODO 1 : finish this class

    # HINT look up/use the module heapq.

    def __init__(self):
        self.queue = []
        self.current = 0

    def next(self):
        if self.current >= len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def pop(self):
        return heapq.heappop(self.queue)

    def remove(self, nodeId):
        self.queue.pop(nodeId)

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]' % (', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue,node)

    def __contains__(self, key):
        self.current = 0
        return key in [n for v, n in self.queue]

    def __eq__(self, other):
        return self == other

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def top(self):
        return self.queue[0]

    __next__ = next


def check_pq():
    ''' check_pq is checking if your PriorityQueue
    is completed or not'''
    pq = PriorityQueue()
    temp_list = []

    for i in range(10):
        a = random.randint(0, 10000)
        pq.append((a, 'a'))
        temp_list.append(a)

    temp_list = sorted(temp_list)

    for i in temp_list:
        j = pq.pop()
        if not i == j[0]:
            return False

    return True


def generate_adjacents(current, word_list):
    ''' word_list is a set which has all words.
    By comparing current and words in the word_list,
    generate adjacents set and return it'''
    adj_set = set()
    # TODO 2: adjacents
    alph = "abcdefghijklmnopqrstuvwxyz"
    wor = current[2]
    for i in range(len(wor)):
        for j in alph:
            word = wor[0:i] + j + wor[i + 1:]
            if word in word_list and word != wor:
                adj_set.add(word)
    return adj_set
    # Return the children words


def dist_heuristic(v, goal):
    ''' v is the current node. Calculate the heuristic function
    and then return a numeric value'''
    # TODO 3: heuristic
    # Calculates the number of characters different between the two words
    dist = 0
    vor = v
    for i in range(len(vor)):
        if vor[i] != goal[i]:
            dist = dist+1
    return dist

def finder(wordNode,lister):
    counter = 0
    for i in lister:
        if len(i[1])>len(wordNode[1]) and wordNode[2]==i[2]:
            return counter
        counter = counter+1
    return -1

def finden(word, listen):
    for i in listen:
        if word == i[2]:
            return True
    return False


def a_star(word_list, start, goal, heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
    Update the cost and path if you find the lower-cost path in your process.
    You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
    '''
    startfrontier = PriorityQueue()
    endfrontier = PriorityQueue()
    explored = set()
    if start == goal: return []
    # TODO 4: A* Search
    startfrontier.append((0,[start],start))
    endfrontier.append((0,[goal],goal))
    diction = {start:0}
    star = False
    end = False
    sta = []
    en = []
    while startfrontier and endfrontier:
        if not star:
            starter = startfrontier.pop()
            if starter[2]==goal or finden(starter[2],endfrontier):
                sta = starter[1]
                sta = True
            for child in generate_adjacents(starter,word_list):
                if child not in explored:
                    startfrontier.append((dist_heuristic(child,goal)+1,starter[1]+[child],child))
            explored.add(starter[2])
        elif star and end: break
        if not end:
            ender = endfrontier.pop()
            if ender[2] == start or finden(ender[2], startfrontier):
                en = ender[1]
                end = True
            for child in generate_adjacents(ender, word_list):
                if child not in explored:
                    endfrontier.append((dist_heuristic(child, start) + 1, ender[1] + [child], child))
            explored.add(ender[2])
        elif star and end: break
    if sta != [] and en != []:
        return sta + en[::-1][1:]
    else:
        return None

def main():
    word_list = set()
    file = open("words_6_longer.txt", "r")
    for word in file.readlines():
        word_list.add(word.rstrip('\n'))
    file.close()
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path_and_steps = (a_star(word_list, initial, goal))
    if path_and_steps != None:
        print(path_and_steps)
        print("steps: ", len(path_and_steps))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()

'''Sample output 1
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
steps:  7
Duration: 0.000997304916381836

Sample output 2
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
steps:  13
Duration: 0.0408782958984375

Sample output 3
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'launch', 'launce', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'banged', 'bunged', 'bungee', 'bungle', 'bingle', 'gingle', 'giggle']
steps:  19
Duration:  0.0867915153503418
'''