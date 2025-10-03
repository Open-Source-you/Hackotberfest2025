#!/usr/bin/env python3
"""
Chaotic ASCII Lifeform
----------------------
- Displays a grid of ASCII "cells" that live/die.
- Every few generations, it *mutates its own rules* randomly.
- No two runs behave the same.
- Press Ctrl+C to stop it.
"""

import os
import random
import time

WIDTH, HEIGHT = 60, 20
ALIVE = "█"
DEAD = " "

def make_grid():
    return [[random.choice([ALIVE, DEAD]) for _ in range(WIDTH)] for _ in range(HEIGHT)]

def count_neighbors(grid, x, y):
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    return sum(
        1 for dx,dy in dirs
        if 0 <= x+dx < WIDTH and 0 <= y+dy < HEIGHT and grid[y+dy][x+dx] == ALIVE
    )

def mutate_rules():
    # Random thresholds for survival/birth
    survive = set(random.sample(range(9), k=random.randint(0, 8)))
    born = set(random.sample(range(9), k=random.randint(0, 8)))
    return survive, born

def next_gen(grid, survive, born):
    new = [[DEAD]*WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            n = count_neighbors(grid, x, y)
            if grid[y][x] == ALIVE and n in survive:
                new[y][x] = ALIVE
            elif grid[y][x] == DEAD and n in born:
                new[y][x] = ALIVE
    return new

def print_grid(grid, generation, survive, born):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Chaotic Lifeform  |  Gen {generation}  |  Rules: survive={survive}, born={born}")
    for row in grid:
        print("".join(row))

def run():
    grid = make_grid()
    survive, born = mutate_rules()
    generation = 0
    try:
        while True:
            if generation % 15 == 0:  # mutate rules every 15 generations
                survive, born = mutate_rules()
            print_grid(grid, generation, survive, born)
            grid = next_gen(grid, survive, born)
            generation += 1
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nSimulation ended.")

if __name__ == "__main__":
    run()
