import tkinter as tk
from tkinter import messagebox
from Algorithms import BFS, DFS, Greedy_best_first_search, A_star, custom1, Problem, ReadFile

# Constants for grid size and colors
CELL_SIZE = 50
DEFAULT_COLOR = "white"
WALL_COLOR = "black"
START_COLOR = "red"
END_COLOR = "green3"
PATH_COLOR = "yellow"

class PathfindingApp(Problem):  # Inherit from the Problem class
    def __init__(self, master):
        super().__init__()  # Initialize the parent class (Problem)
        self.master = master
        self.master.title("Pathfinding GUI")

        # Read the File from RobotNav-test.txt
        ReadFile(self) 
        
        # Set canvas size based on the grid dimensions
        self.canvas_width = len(self.grid[0]) * CELL_SIZE
        self.canvas_height = len(self.grid) * CELL_SIZE
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

           
        self.create_canvas()

        self.algorithm_var = tk.StringVar(value="BFS")
        self.algorithm_menu = tk.OptionMenu(master, self.algorithm_var, "BFS", "DFS", "GDBS", "A*", "Custom1")
        self.algorithm_menu.pack(side=tk.LEFT)


        self.start_button = tk.Button(master, text="Start Pathfinding", command=self.start_pathfinding)
        self.start_button.pack(side=tk.LEFT)
              

        self.end_point_variable = tk.StringVar(value=str(self.end_point))
        self.end_point_menu = tk.OptionMenu(master, self.end_point_variable, *[str(end_point) for end_point in self.goals], command=self.selecting_end_point)
        self.end_point_menu.pack()

        self.set_end_point_button = tk.Button(master, text="Set End Point", command=self.set_end_point)
        self.set_end_point_button.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_canvas)
        self.reset_button.pack()

    def selecting_end_point(self,value):
        
        
        self.end_point = eval(value)
        self.create_canvas()

    def set_end_point(self):
        self.create_canvas()
        self.set_end_point_button.config(state=tk.DISABLED)
        self.canvas.bind("<Button-1>", self.set_end_point_callback)
        self.master.after(100)

    def set_end_point_callback(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if self.grid[y][x] != 1:  # Check if the cell is not a wall
            self.goals.append((y,x))
            self.end_point = (y,x)
            self.end_point_variable.set(str(self.end_point))  # Update the end point variable
            self.end_point_menu['menu'].add_command(label=str(self.end_point), command=lambda value=str(self.end_point): self.end_point_variable.set(value))  # Add the new endpoint to the menu
            self.create_canvas()  # Update the canvas
        self.set_end_point_button.config(state=tk.NORMAL)
        self.canvas.unbind("<Button-1>")
    def create_canvas(self):
        self.canvas.delete("all")  # Clear previous grid
       

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                color = DEFAULT_COLOR
                if self.grid[i][j] == 1:
                    color = WALL_COLOR
                elif (i, j) == self.start_state:
                    color = START_COLOR
                elif (i, j) == self.end_point:
                    color = END_COLOR

                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def start_pathfinding(self):
        end_point = self.end_point_variable.get()
        self.end_point = eval(end_point)


        self.start_button.config(state=tk.DISABLED)

        self.algorithm_menu.config(state=tk.DISABLED)

        

        algorithm = self.algorithm_var.get()
        if algorithm == "BFS":
            path = BFS(self)
        elif algorithm == "DFS":
            path = DFS(self)
        elif algorithm == "GDBS":
            path = Greedy_best_first_search(self)
        elif algorithm == "A*":
            path = A_star(self)
        elif algorithm == "Custom1":
            path = custom1(self)
        else:
            messagebox.showerror("Error", "Unknown algorithm selected")
            return

        self.start_button.config(state=tk.NORMAL)

        self.algorithm_menu.config(state=tk.NORMAL)


        if isinstance(path, list):
            
            self.retrace_path(path)
            path = []
        else:
            messagebox.showinfo("Result", "No path found!")

    def goal_test(self, current):
        
        self.visualize_visited_cells(current)
        return super().goal_test(current)
    
    def visualize_visited_cells(self, visited):
        # Draw all visited cells in gray
        
        x, y = visited
        self.canvas.create_rectangle(y * CELL_SIZE, x * CELL_SIZE,
                                        (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                                        fill="lightgray")
        self.master.update()
        self.master.after(150)  # Delay for visualization

    def retrace_path(self, path):
        # Define the movement directions
        direction_map = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        # Start from the starting position
        current_position = self.start_state  # Use start_state as the starting point
        self.canvas.create_rectangle(current_position[1] * CELL_SIZE, current_position[0] * CELL_SIZE,
                                        (current_position[1] + 1) * CELL_SIZE, (current_position[0] + 1) * CELL_SIZE,
                                        fill=PATH_COLOR)  # Mark start point in yellow
        self.master.update()
        self.master.after(100)

        # Initialize step counter
        step_counter = 1

        # Retrace the path using directions
        for direction in path:
            if direction in direction_map:
                move = direction_map[direction]
                current_position = (current_position[0] + move[0], current_position[1] + move[1])

                # Draw the current position
                self.canvas.create_rectangle(current_position[1] * CELL_SIZE, current_position[0] * CELL_SIZE,
                                                (current_position[1] + 1) * CELL_SIZE, (current_position[0] + 1) * CELL_SIZE,
                                                fill=PATH_COLOR)  # Mark each step in yellow

                # Add step number
                self.canvas.create_text((current_position[1] + 0.5) * CELL_SIZE, (current_position[0] + 0.5) * CELL_SIZE,
                                            text=str(step_counter), fill="black", font=("Arial", 12))

                # Update the display
                self.master.update()
                self.master.after(100)  # Delay for visualization

                # Increment the step counter
                step_counter += 1

    def reset_canvas(self):
        self.create_canvas()  # Redraw the grid to clear the previous state

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()