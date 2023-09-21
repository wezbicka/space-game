import time
import random
import asyncio
import os
import statistics

import curses
from itertools import cycle

import fire_animation
from curses_tools import draw_frame, \
    read_controls, get_frame_size


TIC_TIMEOUT = 0.1


def get_frames(folder="spaceship"):
    frames = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r') as file:
            frames.append(file.read())
    return frames

def draw(canvas):
    canvas.nodelay(True)
    symbols = "*.○+●°•☆:☼★٭✽❇❈❉❊❋⁂"
    curses.curs_set(False)
    canvas.border()
    window_y, window_x = canvas.getmaxyx()
    coroutines = []
    frames = get_frames()
    coroutines.append(animate_spaceship(canvas, window_y//2, window_x//2, frames))

    for i in range(100):
        coroutines.append(blink(
            canvas,
            random.randint(1, window_y-5),
            random.randint(1, window_x-5),
            random.randint(0, 3),
            random.choice(symbols),
        ))
    
    fire_coroutine = fire_animation.fire(
        canvas,
        window_y//2,
        window_x//2,
    )
    coroutines.append(fire_coroutine)
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


async def animate_spaceship(canvas, row, column, frames):
    canvas.nodelay(True)
    screen_max_y, screen_max_x = canvas.getmaxyx()
    for frame in cycle(frames):
        height, width = get_frame_size(frame) 
        frame_max_row, frame_max_column = screen_max_y - height, screen_max_x - width
        
        x_direction, y_direction, space_pressed = read_controls(canvas)
        
        row += x_direction
        column += y_direction

        row = statistics.median([1, row, frame_max_row - 1])
        column = statistics.median([1, column, frame_max_column - 1])
      
        draw_frame(canvas, row, column, frame)
        canvas.refresh()
        await asyncio.sleep(0)
        # стираем предыдущий кадр, прежде чем рисовать новый
        draw_frame(canvas, row, column, frame, negative=True)


async def blink(canvas, row, column, seconds, symbol='*'):
    while True:
        for _ in range(seconds):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
