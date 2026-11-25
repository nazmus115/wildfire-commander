import tkinter as tk
import random
from collections import deque

CELL = 40 # each grid square 40 pixels wide and long
SIZE = 14 # the board have SIZE rows and colums 
FOREST, BREAK, FIRE, BURNT, VILLAGE = range(5) # sets forest = 0, break = 1 and so on
BREAKS_PER_TURN = 2
breaks_left = BREAKS_PER_TURN
SPREAD_CHANCE = 0.75
fire_queue = deque([(1, 1)])
turn = 0

COLORS = {
    FOREST: "#3b8a3e",
    BREAK: "#c8b27a",
    FIRE: "#f08a1c",
    BURNT: "#3a3a3a",
    VILLAGE: "#d94a4a",
}

root = tk.Tk()
root.title("Wildfire Commander DS Project")
canvas = tk.Canvas(root, width=SIZE*CELL, height=SIZE*CELL)
canvas.pack()
status = tk.Label(root, font=("Helvetica", 12))
status.pack()

grid = [[FOREST] * SIZE for _ in range(SIZE)]

for r in (10, 11): # this sets the village coordiantes and colors it as village
    for c in (10, 11):
        grid[r][c] = VILLAGE
        
grid[1][1] = FIRE # hardcoded the fire to always spawn here

def neighbors(r,c): # this function returns the neighbors of a given cell (up down left right)
    result = []
    for drow, dcol in ((1,0), (-1,0), (0,1), (0, -1)):
        nrow = r + drow
        ncol = c + dcol
        if 0 <= nrow < SIZE and 0 <= ncol < SIZE:
            result.append((nrow,ncol))
    return result

# for nr,nc in neighbors(1,1):
#     grid[nr][nc] = BURNT

def place_break(r,c): # this function selects a cell and saves it from burning
    global breaks_left
    if breaks_left == 0:
        return False
    if grid[r][c] != FOREST:
        return False
    grid[r][c] = BREAK
    breaks_left -= 1
    return True

def on_click(event): # this function lets draw firebreak cell 
    r = event.y // CELL
    c = event.x // CELL
    
    if place_break(r, c):
        draw()

def draw():
    canvas.delete("all")
    for r in range(SIZE):
        for c in range(SIZE):
            x = c * CELL
            y = r * CELL
            canvas.create_rectangle(x, y , x + CELL, y + CELL, fill=COLORS[grid[r][c]], outline="#1f1f1f")
        status.config(text=f"Turn {turn}   Firebreaks left: {breaks_left}   Fire front: {len(fire_queue)}")
    
def next_turn():
    global fire_queue, breaks_left, turn
    
    new_front = deque()
    while fire_queue:
        r,c = fire_queue.popleft()
        for nr, nc in neighbors(r ,c):
            if grid[nr][nc] in (FOREST, VILLAGE):
                if random.random() < SPREAD_CHANCE:
                    grid[nr][nc] = FIRE
                    new_front.append((nr,nc))
        grid[r][c] = BURNT
    fire_queue = new_front
    breaks_left = BREAKS_PER_TURN
    turn += 1
    draw()

tk.Button(root, text="Next turn", command=next_turn).pack()
root.bind("<space>", lambda e: next_turn())

canvas.bind("<Button-1>", on_click)
draw()
root.mainloop()