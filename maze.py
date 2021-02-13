'''
Quick note to anyone reading this. I am still working on this code.
Still trying to understand why it isn't doing what I expect.
'''
import pygame, sys
from pygame.locals import *
from random import choice

pygame.init()
clock = pygame.time.Clock()

WINSIZE = (600, 400)
WIN = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('Maze generator / Solver')

maze = []  # The 2D list to represent our maze
stack = []  # The stack to determine the order in which the cells are visited
gap = 1
max_row = 14
max_col = 20
size = int(WINSIZE[0] / max_col), int(WINSIZE[1] / max_row)
background = (25, 50, 25)

def build_grid(row, col):
    '''
    Builds the grid given the number or rows and columns.
    '''
    global maze, untouched
    maze = [[] for i in range(row)]
    for i in range(row):
        for j in range(col):
            cell = (i, j)
            maze[i].append(cell)

def generate_maze(active_cell):
    global maze, stack
    row, col = active_cell
    stack.append(active_cell)

    up = row - 1, col
    down = row + 1, col
    right = row, col + 1
    left = row, col - 1

    unvisited = []
    if up not in stack and 0 <= up[0] < max_row and 0 <= up[1] < max_col:
        unvisited.append(up)
    if down not in stack and 0 <= down[0] < max_row and 0 <= down[1] < max_col:
        unvisited.append(down)
    if right not in stack and 0 <= right[0] < max_row and 0 <= right[1] < max_col:
        unvisited.append(right)
    if left not in stack and 0 <= left[0] < max_row and 0 <= left[1] < max_col:
        unvisited.append(left)
    
    while unvisited:
        cell = choice(unvisited)
        # stack.append(cell)
        generate_maze(cell)
        unvisited.remove(cell)

def move_up(cell):
    row, col = cell
    rect = pygame.Rect(col * size[0] + gap, (row - 1) * size[1] + gap, size[0] - gap * 2, size[1] * 2 - gap * 2)
    pygame.draw.rect(WIN, maze_color, rect, 0)
    
def move_down(cell):
    row, col = cell
    rect = pygame.Rect(col * size[0] + gap, (row) * size[1] + gap, size[0] - gap * 2, size[1] * 2 - gap * 2)
    pygame.draw.rect(WIN, maze_color, rect, 0)
    
def move_right(cell):
    row, col = cell
    rect = pygame.Rect(col * size[0] + gap, (row) * size[1] + gap, size[0] * 2 - gap * 2, size[1] - gap * 2)
    pygame.draw.rect(WIN, maze_color, rect, 0)
    
def move_left(cell):
    row, col = cell
    rect = pygame.Rect((col - 1) * size[0] + gap, row * size[1] + gap, size[0] * 2 - gap * 2, size[1] - gap * 2)
    pygame.draw.rect(WIN, maze_color, rect, 0)

def up(cell):
    row, col = cell
    return (row - 1, col)

def down(cell):
    row, col = cell
    return (row + 1, col)

def right(cell):
    row, col = cell
    return (row, col + 1)

def left(cell):
    row, col = cell
    return (row, col - 1)

def neighbours(cell):
    row, col = cell
    up = (row - 1, col)
    down = (row + 1, col)
    right = (row, col + 1)
    left = (row, col - 1)
    return (up, down, left, right)

maze_color = (0, 0, 255)
wall_color = (0, 0,   0)
drew = []

def draw_maze(cell=(0, 0), drawn=[]):
    global maze, stack
    
    if cell == (0, 0):
        WIN.fill(background)
        for row in maze:
            for cell in row:
                row, col = cell
                rect = pygame.Rect(size[0] * col, size[1] * row, size[0], size[1])
                pygame.draw.rect(WIN, maze_color, (rect.x + gap, rect.y + gap, size[0] - gap * 2, size[1] - gap * 2), 0)
                pygame.draw.rect(WIN, wall_color, rect, gap)
    drawn.append(cell)
    drew.append(cell)
    nxt_cell = None
    for any_cell in stack:
        if any_cell not in drawn:
            nxt_cell = any_cell
            break

    if nxt_cell == None or nxt_cell not in neighbours(cell):
        
        print(nxt_cell, '== next_cell')
        print(cell, '== cell')
        print('I am here')
        print(drawn, '== drawn')
        return
    else:

    
        if nxt_cell == up(cell):
            print('I moved up')
            move_up(cell)
            
        elif nxt_cell == down(cell):
            move_down(cell)
            print('I moved down')
        elif nxt_cell == left(cell):
            move_left(cell)
        else:  # nxt_cell == right(cell):
            move_right(cell)
            print('I moved right')

    cell = nxt_cell
    
    while cell != None:
        draw_maze(cell, drawn)

        cell = None
        for visited_cell in stack:
            if visited_cell not in drawn:
                cell = visited_cell
                break
    print('I am true')
    

build_grid(max_row, max_col)
generate_maze((0, 0))
WIN.fill(background)
draw_maze(cell=(0, 0), drawn=[])
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()
