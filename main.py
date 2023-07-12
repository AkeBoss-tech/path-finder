from random import random
import pygame

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 900
HEIGHT = 600
ROWS = int(input("Enter the number of rows (50 is nice)\n> "))
COLS = int(input("Enter the number of rows (50 is nice)\n> "))

inp = input("Would you like to use euclidean (diagonal) distance instead of taxicab distance for A*? (y/n)\n> ").strip().lower()
TAXICAB_HEURISTIC = True
if inp == "y":
    TAXICAB_HEURISTIC = False

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
colors = [WHITE, BLACK, GREEN, RED, YELLOW, GRAY, BLUE, PURPLE, ORANGE, TURQUOISE, YELLOW, MAGENTA]


# Dimensions
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Environment array
environment = [[0] * COLS for _ in range(ROWS)]  # 0 represents empty, 1 represents boundary

# Start position
start_pos = ()
end_pos = ()

# Mouse state
mouse_down = False

# Draw the environment grid
def draw_environment():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if environment[row][col] == 1 else BLACK
            if environment[row][col] == 3:
                color = GREEN
            elif environment[row][col] == 2:
                color = RED
            drawSquare((col, row), color)

def drawSquare(pos: tuple, color: tuple):
    pygame.draw.rect(WIN, color, (pos[0] * CELL_WIDTH, pos[1] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                        

# Remove the start position
def remove_start_pos():
    global start_pos
    if start_pos != ():
        environment[start_pos[0]][start_pos[1]] = 0
        start_pos = ()

# Remove the end position
def remove_end_pos():
    global end_pos
    if end_pos != ():
        environment[end_pos[0]][end_pos[1]] = 0
        end_pos = ()

# Swap the value of a cell
def swap(value):
    return 0 if value == 1 else 1

openSet = []
closedSet = []

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.wall = True if environment[y][x] == 1 else False

    def show(self, draw, color):
        if self.wall:
            color = WHITE
        if (self.y, self.x) == start_pos:
            color = GREEN
        if (self.y, self.x) == end_pos:
            color = RED
        draw((self.x, self.y), color)

    def get_neighbors(self) -> list:
        if (self.x > 0):
            self.neighbors.append(Node(self.x - 1, self.y))
        if (self.x < COLS - 1):
            self.neighbors.append(Node(self.x + 1, self.y))
        if (self.y > 0):
            self.neighbors.append(Node(self.x, self.y - 1))
        if (self.y < ROWS - 1):
            self.neighbors.append(Node(self.x, self.y + 1))

        if (self.x > 0) and (self.y > 0):
            self.neighbors.append(Node(self.x - 1, self.y - 1))
        if (self.x < COLS - 1) and (self.y > 0):
            self.neighbors.append(Node(self.x + 1, self.y - 1))
        if (self.x > 0) and (self.y < ROWS - 1):
            self.neighbors.append(Node(self.x - 1, self.y + 1))
        if (self.x < COLS - 1) and (self.y < ROWS - 1):
            self.neighbors.append(Node(self.x + 1, self.y + 1))
        return self.neighbors
    
    def checkIfDiagonal(self, __o: object) -> bool:
        return (self.x != __o.x) and (self.y != __o.y)

    def __eq__(self, __o: object) -> bool:
        return (self.x == __o.x) and (self.y == __o.y)
    
    def __repr__(self) -> str:
        return f"Node({self.x}, {self.y})"

def heuristic(a: Node, b: Node) -> float:
    # Taxicab distance
    if TAXICAB_HEURISTIC:
        return abs(a.x - b.x) + abs(a.y - b.y)
    # Euclidean distance
    return (a.x - b.x)**2 + (a.y - b.y)**2
    

def aStarSearch(start, end, draw) -> list:
    global openSet, closedSet
    openSet.append(start)

    while len(openSet) > 0:
        # Get the node with the lowest f score
        lowest_score = min(openSet, key=lambda node: node.f)
        path = []
        temp = lowest_score
        while temp.previous:
            path.append(temp.previous)
            temp = temp.previous
        
        for nodes in path:
            nodes.show(draw, YELLOW)
        
        if lowest_score == end:
            # Get path
            pygame.display.update()
            print("The path is " + str(lowest_score.f) + " units long.")
            print("Found the end!")
            return path
        
        closedSet.append(lowest_score)
        openSet.remove(lowest_score)

        for neighbor in lowest_score.get_neighbors():
            if neighbor in closedSet or neighbor.wall:
                continue
            tempG = lowest_score.g + (1 if not neighbor.checkIfDiagonal(lowest_score) else 1.5)
            if neighbor in openSet:
                if tempG < neighbor.g:
                    neighbor.g = tempG
            else:
                neighbor.g = tempG
                openSet.append(neighbor)

            neighbor.h = heuristic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.previous = lowest_score
            
        # show closed set
        for node in closedSet:
            node.show(draw, TURQUOISE)
        
        # show open set
        for node in openSet:
            node.show(draw, GRAY)
            
        # delay
        # pygame.time.delay(1)
        pygame.display.update()
    else:
        print("No solution")
        return []

def drawCar(pos: tuple):
    pygame.draw.circle(WIN, RED, pos, 20)


# Main loop
def main():
    global mouse_down, start_pos, end_pos, WIN
    run = True

    inp = input("Would you like a random environment? (y/n)\n> ").strip().lower()
    if inp == "y":
        prob = float(input("Enter the probability of a cell being a boundary (0-1)\n> "))
        # Generate random environment
        for row in range(ROWS):
            for col in range(COLS):
                environment[row][col] = 1 if random() < prob else 0

    print("Controls:")
    print("Left click: Set walls")
    print("Right click: Set start position")
    print("Middle click or scroll: Set end position")
    print("Space: Run algorithm")
    input("Press enter to continue...")

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding")

    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_down = True

                print(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    mouse_down = False
                elif event.button in [2, 4, 5]:  # Scroll wheel button
                    remove_end_pos()
                    end_pos = (pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH)
                    environment[end_pos[0]][end_pos[1]] = 2
                elif event.button == 3: # Right mouse button
                    remove_start_pos()
                    start_pos = (pos[1] // CELL_HEIGHT, pos[0] // CELL_WIDTH)
                    environment[start_pos[0]][start_pos[1]] = 3
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Perform A* algorithm here with the updated environment and start position
                    run = False

        if not run and (start_pos == () or end_pos == () or start_pos == end_pos):
                print("Please set a start and end position.")
                run = True

        if mouse_down:
            col = pos[0] // CELL_WIDTH
            row = pos[1] // CELL_HEIGHT
            environment[row][col] = 1
                
        draw_environment()
        pygame.display.update()

    # Perform A* algorithm here with the updated environment and start position
    start = Node(start_pos[1], start_pos[0])
    end = Node(end_pos[1], end_pos[0])
    path = aStarSearch(start, end, drawSquare)

    print("Enter to exit ...")
    input()
    # print(environment)
    with open("environment.txt", "w") as f:
        for row in environment:
            f.write(str(row) + "\n")
    pygame.quit()

if __name__ == '__main__':
    WIN = None
    main()
