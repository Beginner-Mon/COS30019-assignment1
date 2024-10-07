import sys
from input import Problem
from queue import PriorityQueue

import heapq

# depth first search algorithm
def BFS(prob : Problem):
    num_of_nodes = 0
    queue = [prob.start_state]
    discovered = {prob.start_state: None}
    while len(queue) != 0:

        current = queue.pop(0)
        num_of_nodes += 1
        if prob.goal_test(current):    
            print(f"{current} {num_of_nodes}") 
            path = [current]
            while discovered[current] != None:
                current = discovered[current]
                path.append(current)
            direction = []
            for index in range(len(path)-1,0, -1) :
                direction.append (get_direction(path[index-1], path[index]))
            return direction
            
        for next_state in prob.next_step(current):
            if next_state not in discovered:
                queue.append(next_state)
                discovered[next_state] = current
        
    return "No goal reachable"
    
# depth first search algorithm
def DFS(prob):
    path = []
    discovered  = { prob.start_state:None}
    num_of_nodes = [0]
    check = calculateDFS(prob,num_of_nodes,prob.start_state, prob.end_point, discovered,path)
    if check:
        return path
    else:
        return "No goal Reachable"
    
def calculateDFS(prob : Problem,num_of_nodes,  current,end_point , discovered = { }, path = []):
    num_of_nodes[0] += 1
    if prob.goal_test(current): 
        print(f"{current} {num_of_nodes[0]}")
        return True
    
    for next_state in prob.next_step(current):
        if next_state not in discovered:            
            discovered[next_state] = current  
                 
            if calculateDFS(prob,num_of_nodes,next_state, end_point, discovered,path):
                path.insert(0,get_direction(next_state,discovered[next_state]))     
                return True
           
              
        
            
# greedy best first search algorithm 
def Greedy_best_first_search( prob: Problem):
    num_of_nodes = 0
    queue = PriorityQueue()
    discovered = {prob.start_state: None}
    queue.put((0,prob.start_state))
    while queue.empty() == False:
        current = queue.get()[1]
        num_of_nodes += 1
        if prob.goal_test(current ):
            print(f"{current} {num_of_nodes}")
            path = [current]
            while discovered[current] != None:
                current = discovered[current]
                path.append(current)
            
            direction = []
            for index in range(len(path)-1,0, -1) :
                direction.append (get_direction(path[index-1], path[index]))
            return direction
        
        for next_state in prob.next_step(current):
            
            if next_state not in discovered:
                queue.put((prob.cost(next_state) , next_state))
                discovered[next_state] = current
    return "No goal Reachable"
# A star algorithm
def A_star(prob : Problem):
    num_of_nodes = 0
    queue = []
    g = [[0 for _ in range(len(prob.grid))] for _ in range(len(prob.grid[0]))]
    f = [[0 for _ in range(len(prob.grid))] for _ in range(len(prob.grid[0]))]
    discovered = {prob.start_state: None}
    heapq.heappush(queue, (0, prob.start_state))
    while queue:
        current = heapq.heappop(queue)[1]
        num_of_nodes += 1
        if prob.goal_test(current):
            print(f"{current} {num_of_nodes}")
            path = [current]
            while discovered[current] != None:
                current = discovered[current]
                path.append(current)
            
            direction = []
            for index in range(len(path)-1,0, -1) :
                direction.append (get_direction(path[index-1], path[index]))
            return direction
        
        for next_state in prob.next_step(current):
            if  next_state not in discovered:
                discovered[next_state] = current
                curr_x = next_state[1]
                curr_y = next_state[0]
                h = prob.cost(next_state)
                g_new = g[current[1]][current[0]] + 1
                f_new =  + h

                if f[curr_x][curr_y] == 0 or f[curr_y][curr_x] > f:
                    g[curr_x][curr_y] = g_new
                    f[curr_x][curr_y] = f_new
                    heapq.heappush(queue, (f_new, next_state))


    return "No goal Reachable"
# get the heuristic function h(n) 

def custom1(prob : Problem):
    
    queue = [prob.start_state]
    discovered  = { prob.start_state : None}
    while queue:
        current = queue.pop()
        
        if fast_travel(prob,current, prob.end_point):
            # print(prob.end_point)
            discovered[prob.end_point] = current
            current = prob.end_point
        
        if prob.goal_test(current):
            path = [current]
            fdirection = fast_direction(discovered[current], prob.end_point)
            while discovered[current] != None:
                current = discovered[current]
                path.append(current)
            
            direction = []
            
            for index in range(len(path)-1,1, -1) :
                direction.append(get_direction(path[index-1], path[index]))
            return direction + fdirection
        for next_state in prob.next_step(current):
            if next_state not in discovered:
                discovered[next_state] = current
                queue.append(next_state)

    return "No goal Reachable"

def fast_travel(prob:Problem, current, end_point):
    check = True
    dist_y, dist_x = end_point[0] - current[0], end_point[1] - current[1]
    if dist_x > 0:
        row_slice = prob.grid[current[0]][current[1]:current[1] + dist_x]
        
    elif dist_x <0:
        row_slice = prob.grid[end_point[0]][end_point[1]:end_point[1] + dist_x]
    else:
        row_slice = [0]
    check &= 1 not in row_slice

    if dist_y > 0:
        choosen_column = [row[current[0]] for row in prob.grid]

        column_slice = prob.grid[current[1]: current[1] + dist_y]
    elif dist_y < 0:
        choosen_column = [row[end_point[0]] for row in prob.grid]

        column_slice = prob.grid[end_point[1]: end_point[1] + dist_y]
    else: 
        column_slice = [0]
    
    check &= 1 not in column_slice
    return check

def fast_direction(current, end_point):
    path = []
    
    dist_x = end_point[1] - current[1]
    path += ["right"] * dist_x if dist_x > 0 else ["left"] * abs(dist_x)
    
    dist_y = end_point[0] - current[0]
    path += ["up"] * abs(dist_y) if dist_y < 0 else ["down"] * dist_y
    return path





# define direction from 2 states
def get_direction(pos1: tuple, pos2: tuple):
    direction = {(1,0): "up", (0,1): "left", (-1,0): "down", (0,-1): "right"}
    return direction[(pos2[0]- pos1[0], pos2[1] -pos1[1])]


def to_int(num):
    return int(num)

def ReadFile(test : Problem):
    with open(test.file, "r") as f:
        # get the length of grid n * m
        line1 = f.readline().strip()
        line1 = line1[1:-1].split(",")
        test.grid = [[0 for _ in range (int(line1[1]))] for _ in range(int(line1[0]))] 

        # get the start point
        line2 = f.readline().strip()
        line2 = line2[1:-1].split(",")
        test.start_state = tuple (map(to_int ,line2))[::-1]

        # get the goals
        a = f.readline().strip().split("|")
        for i in a:
            test.goals.append( tuple (map( to_int, i.strip()[1:-1].split(",")))[::-1])
        test.end_point = test.goals[0]

        # get obstacles
        for line in f:
            obstacle = [int(x) for x in line.strip()[1:-1].split(",")]
            wide = int(obstacle[2])
            depth = int(obstacle[3])
            for i in range (wide):      
                for j in range (depth):
                    test.grid[obstacle[1] + j][obstacle[0] + i] = 1

def main():
    test = Problem()
    selection = ""

    # try getting the file text
    try:
        test.file = sys.argv[1]
        
    except IndexError:
        print("you have not typed the file text")
        return

    try:
        selection = sys.argv[2]
    except IndexError:
        print("You have not typed the method")
        return

    
    ReadFile(test)
    test.PrintFile()

    match selection:
        case "BFS":
            print("Breadth-first Search")
            path = BFS(test)
        case "DFS":
            print("Depth-first Search")
            path = DFS(test)
        case "GBFS":
            print("Greedy Best-first Search")
            path = Greedy_best_first_search(test)
        case "A*":
            print("A star algorithm search")
            path =A_star(test)
        case "CS1":
            print("Custom 1 Search")
            path = custom1(test)
        case _:
            print(f"there is no method with the name {selection}")
            return

    print(f"File Name: {test.file}")
    print(path)
  
    
if __name__ == "__main__":
    main()