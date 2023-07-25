import time
import random
import asyncio
import os

import curses
from itertools import cycle

import fire_animation
from curses_tools import draw_frame, read_controls


TIC_TIMEOUT = 0.1


def draw(canvas):
    
    folder = "spaceship"
    with open(os.path.join(folder, "rocket_frame_1.txt"), "r") as content:
        frame1 = content.read()
    with open(os.path.join(folder, "rocket_frame_2.txt"), "r") as content:
        frame2 = content.read()
    frames = [frame1, frame2]
  
    symbols = "*.○+●°•☆:☼★٭✽❇❈❉❊❋⁂"
    curses.curs_set(False)
    canvas.border()
    window_y, window_x = canvas.getmaxyx()
    coroutines = []
    coroutines.append(animate_spaceship(canvas, window_y//2, window_x//2, frames))

    for i in range(100):
        coroutines.append(blink(
            canvas,
            random.randint(1, window_y-5),
            random.randint(1, window_x-5),
            random.randint(0, 3),
            random.choice(symbols),
        ))
    
    fire_corutine = fire_animation.fire(
        canvas,
        window_y//2,
        window_x//2,
    )
    coroutines.append(fire_corutine)
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
    for frame in cycle(frames):
        rows_direction, columns_direction, _ = read_controls(canvas)
        row += rows_direction
        column += columns_direction
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
