import sys
import math

class Problem:
    def __init__(self, file = "RobotNav-test.txt") -> None:
        
        self.start_state = None
        self.goals = []
        self.grid = None
        self.file = file
        self.end_point = None
    def PrintFile(self):
        for i in self.grid:

            for j in i:
                print(j, end = " ")

            print()
        
    def goal_test(self, current):
        
        return current == self.end_point
    

    def is_position_valid(self,position) -> bool:
        x,y = position 
        if 0 <= x < len(self.grid) and 0<= y < len(self.grid[0]) and self.grid[x][y] != 1:
            return True
        
    def next_step(self,position):
        x, y = position
        states = []
        for dx,dy in [(-1,0),(0,-1), (1,0), (0,1) ]:
            nx = x +dx
            ny = y + dy
            if self.is_position_valid((nx,ny)):
                states.append((nx,ny))
        return states
    
    def cost(self, current):
        return math.sqrt((self.end_point[1] - current[1]) ** 2 + (self.end_point[0] - current[0]) ** 2 )

def main():
    test = Problem()



    
    
if __name__ == "__main__":
    main()