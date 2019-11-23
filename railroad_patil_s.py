# Name: Somu Patil       Data: 11/4/2018
import heapq, random, pickle, math, time
from math import pi, acos , sin , cos

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

'''Making class Graph(), Node(), and Edge() are optional'''
'''You can make any helper methods'''
def calcd(y1,x1, y2,x2):
   #
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees

   # if (and only if) the input is strings
   # use the following conversions

   y1  = float(y1)
   x1  = float(x1)
   y2  = float(y2)
   x2  = float(x2)
   #
   R   = 3958.76 # miles = 6371 km
   #
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0
   #
   # approximate great circle distance with law of cosines
   #
   return acos(min((sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)),1)) * R
   #

def make_graph(nodes_file, node_city_file, edge_file):
   NCity = {}
   CityN = {}
   Loc = {}
   Edges = {}
   Neighbors = {}
   file = open(node_city_file,"r")
   cit = file.readlines()
   for line in cit:
       node,city = line.split(" ",1)
       city = city.replace("\n","")
       NCity[node] = city
       CityN[city] = node
   file = open(nodes_file,"r")
   cit = file.readlines()
   for line in cit:
       node,lat,long = line.split()
       Loc[node] = (lat,long)
   file = open(edge_file,"r")
   cit = file.readlines()
   for line in cit:
       one,two = line.split()
       Edges[(one,two)] = calc_edge_cost(one,two,Loc)
       Edges[(two,one)] = calc_edge_cost(two,one,Loc)
       if one not in Neighbors.keys():
           Neighbors[one] = set()
           Neighbors[one].add(two)
       else:
           Neighbors[one].add(two)
       if two not in Neighbors.keys():
           Neighbors[two] = set()
           Neighbors[two].add(one)
       else:
           Neighbors[two].add(one)
   return [NCity, CityN, Loc, Edges, Neighbors]

def calc_edge_cost(start, end, loc):
   # TODO: calculate the edge cost from start city to end city
   y1, x1 = loc[start]
   y2, x2 = loc[end]
   return calcd(y1,x1,y2,x2)

def breadth_first_search(start, goal, graph):
   # TODO: finish this method
   frontier = [graph[1][start]] # Initialize frontier with the id of the start city
   goal = graph[1][goal] # Reset the goal to the id of the goal
   explored = {graph[1][start]:"s"} # Set the parent of start with no parent in the explored dictionary
   nodes = 0
   while frontier:
       a = frontier.pop(0)
       nodes += 1
       if a == goal:
           lis = []
           cost = 0
           while a != "s":
               lis.append(a)
               if explored[a] != "s":
                   cost += graph[3][(explored[a],a)] # Adding the edge costs of all edges in the path
               a = explored[a]
           lis = lis[::-1]
           return displaynodes(lis,graph,nodes,cost) # Calling the displaynodes method, passing graph as a parameter
       else:
           for child in graph[4][a]: # iterating through all of the adjacent ids
               if child not in explored:
                   frontier.append(child)
                   explored[child] = a
   return "No solution"

def dist_heuristic(v, goal, graph):
   # TODO: calculate the heuristic value from node v to the goal
   return calc_edge_cost(v,goal,graph[2]) # Calculate the edge cost from current node to goal

def displaynodes(lis,graph,nodes,cost):
    print("cost: ",end="")
    print(cost)
    print("node path: ", end="")
    print(lis)
    print("number of explored nodes: ", end="")
    print(nodes)
    cities = []
    for node in lis:
        if node in graph[0]: # checking if the node is in the NodeToCity dictionary
            cities.append(graph[0][node]) # Append the city into the city list
    return cities

def a_star(start, goal, graph, heuristic=dist_heuristic):
   # TODO: Implement A* search algorithm
   frontier = PriorityQueue()
   explored = set()
   frontier.append((0, 0, 0, [graph[1][start]], graph[1][start])) # Initializing frontier with the node containing the id of the start city
   start = graph[1][start] # Reseting start to the id of start
   goal = graph[1][goal] # Reseting goal to the start of goal
   nodes = 0
   while frontier:
       currNode = frontier.pop()
       nodes += 1
       if len(currNode[3]) > 0 and currNode[4] == goal:
           cost = 0
           for i in range(len(currNode[3]) - 1):
               cost += graph[3][(currNode[3][i], currNode[3][i + 1])] # Adding the edge costs of all edges in the path
           return displaynodes(currNode[3], graph, nodes, cost) # Calling the displaynodes method, passing graph as a parameter
       else:
           explored.add(currNode[4])
           for child in graph[4][currNode[4]]: # Iterating through all the neighbors of the current town/id
               if child not in explored:
                   path = currNode[1] + graph[3][(currNode[4], child)] # Generating the path of the child using the previous path + current node -> child
                   heu = dist_heuristic(child, goal, graph)
                   comb = path + heu
                   node = (comb, path, heu, currNode[3] + [child], child)
                   b = finder(node,frontier)
                   if b!=None:
                       if comb >= b[0]:
                           continue
                   frontier.append(node)
   return []

def speca_star(start, goal, graph, heuristic=dist_heuristic): #same as A*, used in tridirectional search
   # TODO: Implement A* search algorithm
   frontier = PriorityQueue()
   explored = set()
   frontier.append((0, 0, 0, [graph[1][start]], graph[1][start]))
   start = graph[1][start]
   goal = graph[1][goal]
   nodes = 0
   while frontier:
       currNode = frontier.pop()
       nodes += 1
       if len(currNode[3]) > 0 and currNode[4] == goal:
           cost = 0
           for i in range(len(currNode[3]) - 1):
               cost += graph[3][(currNode[3][i], currNode[3][i + 1])]
           return (currNode[3],cost,nodes)
       else:
           explored.add(currNode[4])
           for child in graph[4][currNode[4]]:
               if child not in explored:
                   path = currNode[1] + graph[3][(currNode[4], child)]
                   heu = dist_heuristic(child, goal, graph)
                   comb = path + heu
                   node = (comb, path, heu, currNode[3] + [child], child)
                   b = finder(node,frontier)
                   if b!=None:
                       if comb >= b[0]:
                           continue
                   frontier.append(node)
   return []

def finder(node,lis):
    for nod in lis.queue:
        if node[4]==nod[4]:
            return nod
    return None

def bidirectional_BFS(start, goal, graph):
   # TODO: Implement bi-directional BFS
   frontier = [graph[1][start]] # Initialize frontier with id of the start city
   st = graph[1][start] # Reset start to the id of itself
   frontierend = [graph[1][goal]] # Initialize frontierend with id of the end city
   goal = graph[1][goal] # Reset goal to the id of itself
   explored = {st:"s"}
   exploredend = {goal:"s"}
   nodes = 0
   while frontier and frontierend:
       if frontier:
         a = frontier.pop(0)
         nodes += 1
         if a == goal or a in frontierend:
             ex = a
             exp = a
             listo = []
             listend = []
             while ex != "s":
                 listo.append(ex)
                 ex = explored[ex]
             listo = listo[::-1]
             exp = exploredend[exp]
             while exp != "s":
                 listo.append(exp)
                 exp = exploredend[exp]
             cost = 0
             for i in range(len(listo)-1):
                 cost += graph[3][(listo[i],listo[i+1])] # Sum up all the edge costs between neighbors
             return displaynodes(listo,graph,nodes,cost)
         else:
             for child in graph[4][a]: # Iterate through current node's neighborz
                 if child not in explored:
                     frontier.append(child)
                     explored[child] = a
       if frontierend:
           a = frontierend.pop(0)
           nodes += 1
           if a == st or a in frontier:
               ex = a
               exp = a
               listo = []
               listend = []
               while ex != "s":
                   listo.append(ex)
                   ex = explored[ex]
               listo = listo[::-1]
               exp = exploredend[exp]
               while exp != "s":
                   listo.append(exp)
                   exp = exploredend[exp]
               cost = 0
               for i in range(len(listo) - 1):
                   cost += graph[3][(listo[i], listo[i + 1])] # Summing up all the costs of the edges in the path
               return displaynodes(listo, graph,nodes, cost)
           else:
               for child in graph[4][a]: # Iterating through current node's neighbors
                   if child not in exploredend:
                       frontierend.append(child)
                       exploredend[child] = a
   return []



def bidirectional_a_star(start, goal, graph, heuristic=dist_heuristic):
   # TODO: Implement bi-directional A*
   frontier = PriorityQueue()
   frontierend = PriorityQueue()
   frontier.append((0, 0, 0, [graph[1][start]], graph[1][start])) # Initializing the frontier with the start node
   frontierend.append((0, 0, 0, [graph[1][goal]], graph[1][goal])) # Initializing the frontierend with the end node
   start = graph[1][start] # Resetting start with id
   goal = graph[1][goal] # Resetting end with id
   explored = set()
   exploredend = set()
   nodes = 0
   while frontier and frontierend:
       if frontier:
           a = frontier.pop()
           nodes += 1
           check = finder(a,frontierend)
           if a == goal or check!=None:
               if a == goal:
                   cost = 0
                   for i in range(len(a[3]) - 1):
                       cost += graph[3][(a[3][i], a[3][i + 1])]
                   return displaynodes(a[3], graph,nodes, cost)
               else:
                   mincost = a[1]+check[1]
                   minpath = a[3][:len(a[3])-1]+check[3][::-1]
                   while frontier.size()>0:
                       node = frontier.pop()
                       if node[4] == check[4]:
                           cost = node[1]+check[1]
                           pat = node[3][:len(node[3])-1]+check[3][::-1]
                           if cost < mincost:
                               mincost = cost
                               minpath = pat
                   real = 0
                   for i in range(len(minpath) - 1):
                       real += graph[3][(minpath[i], minpath[i + 1])] # Summing up the costs of the shortest path found
                   return displaynodes(minpath, graph,nodes, real)

           else:
               explored.add(a[4])
               for child in graph[4][a[4]]: #Iterating through all the children
                   if child not in explored:
                       path = a[1] + graph[3][(a[4], child)] # Calculating the path to child
                       heu = dist_heuristic(child, goal, graph) # calculating the heuristic
                       comb = path + heu
                       node = (comb, path, heu, a[3] + [child], child) #Appending the new node into the frontier
                       b = finder(node, frontier)
                       if b != None:
                           if comb >= b[0]:
                               continue
                       frontier.append(node)
       if frontierend: # Same function above except on frontierend
           a = frontierend.pop()
           nodes += 1
           check = finder(a,frontier)
           if a == start or check!=None:
               if a == start:
                   lis = a[3][::-1]
                   cost = 0
                   for i in range(len(a[3]) - 1):
                       cost += graph[3][(lis[i], lis[i + 1])]
                   return displaynodes(lis, graph,nodes, cost)
               else:
                   mincost = a[1]+check[1]
                   minpath = a[3][:len(a[3])-1]+check[3][::-1]
                   while frontierend.size()>0:
                       node = frontierend.pop()
                       if node[4] == check[4]:
                           cost = node[1]+check[1]
                           pat = check[3][:len(check[3])-1]+node[3][::-1]
                           if cost < mincost:
                               mincost = cost
                               minpath = pat
                   real = 0
                   for i in range(len(minpath) - 1):
                       real += graph[3][(minpath[i], minpath[i + 1])]
                   return displaynodes(minpath, graph,nodes, real)

           else:
               exploredend.add(a[4])
               for child in graph[4][a[4]]:
                   if child not in explored:
                       path = a[1] + graph[3][(a[4], child)]
                       heu = dist_heuristic(child, start, graph)
                       comb = path + heu
                       node = (comb, path, heu, a[3] + [child], child)
                       b = finder(node, frontierend)
                       if b != None:
                           if comb >= b[0]:
                               continue
                       frontierend.append(node)
   return []

def tridirectional_search(goals, graph, heuristic=0):
   # TODO: Do this! Good luck!
   ab = speca_star(goals[0],goals[1],graph)
   ac = speca_star(goals[0], goals[2], graph)
   ba = speca_star(goals[1], goals[0], graph)
   bc = speca_star(goals[1], goals[2], graph)
   ca = speca_star(goals[2], goals[0], graph)
   cb = speca_star(goals[2], goals[1], graph)

   abc = (ab[0][:len(ab[0])-1]+bc[0],ab[1]+bc[1],ab[2]+bc[2])
   acb = (ac[0][:len(ac[0])-1]+cb[0],ac[1]+cb[1],ac[2]+cb[2])
   bac = (ba[0][:len(ba[0])-1]+ac[0],ba[1]+ac[1],ba[2]+ac[2])
   bca = (bc[0][:len(bc[0])-1]+ca[0],bc[1]+ca[1],bc[2]+ca[2])
   cab = (ca[0][:len(ca[0])-1]+ab[0],ca[1]+ab[1],ca[2]+ab[2])
   cba = (cb[0][:len(cb[0])-1]+ba[0],cb[1]+ba[1],cb[2]+ba[2])

   lis = [acb,bac,bca,cab,cba]
   temp = abc
   for node in lis:
       if node[1]<temp[1]:
           temp = node
   return displaynodes(temp[0],graph,abc[2]+cab[2]+bca[2],temp[1])

   return []

def main():
   start = input("Start city: ")
   goal = input("Goal city: ")

   '''depends on your data setup, you can change this part'''
   graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")
   print ("\nBFS Summary")
   cur_time = time.time()
   bfs_path = breadth_first_search(start, goal, graph)
   next_time = time.time()
   print ("BFS path: ", bfs_path)
   print ("BFS Duration: ", (next_time - cur_time))

   print ("\nA* Search Summary")
   cur_time = time.time()
   a_star_path = a_star(start, goal, graph)
   next_time = time.time()
   print ("A* path: ", a_star_path)
   print ("A* Duration: ", (next_time - cur_time))

   print ("\nBi-directional BFS Summary")
   cur_time = time.time()
   bi_path = bidirectional_BFS(start, goal, graph)
   next_time = time.time()
   print ("Bi-directional BFS path: ", bi_path)
   print ("Bi-directional BFS Duration: ", (next_time - cur_time))

   print ("\nBi-directional A* Summary")
   cur_time = time.time()
   bi_a_path = bidirectional_a_star(start, goal, graph)
   next_time = time.time()
   print ("Bi-directional A* path: ", bi_a_path)
   print ("Bi-directional A* Duration: ", (next_time - cur_time))

   print()
   start = input("City 1: ")
   goal = input("City 2: ")
   mid = input("City 3: ")

   goals = [start,mid,goal]
   print("\nTridirectional Search Summary")
   cur_time = time.time()
   tri_path = tridirectional_search(goals,graph)
   next_time = time.time()
   print("Tridirectional path: ", tri_path)
   print("Tridirectional Duration: ", (next_time - cur_time))
   
   # TODO: check your tridirectional search algorithm here

if __name__ == '__main__':
   main()

'''BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  13268
BFS path:  ['Los Angeles', 'Chicago']
BFS Duration:  0.03057575225830078

A* Search Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  1272
A* path:  ['Los Angeles', 'Chicago']
A* Duration:  0.036072492599487305

Bi-directional BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional BFS path:  ['Los Angeles', 'Chicago']
Bi-directional BFS Duration:  0.0

Bi-directional A* Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional A* path:  ['Los Angeles', 'Tucson', 'Fort Worth', 'Chicago']
Bi-directional A* Duration:  0.0
'''