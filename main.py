import time
import random
import asyncio

import curses


TIC_TIMEOUT = 0.1


def draw(canvas):
    symbols = "*.○+●°•☆:☼★٭✽❇❈❉❊❋⁂"
    curses.curs_set(False)
    canvas.border()
    window_y, window_x = canvas.getmaxyx()
    coroutines = []
    for i in range(100):
        coroutines.append(blink(
            canvas,
            random.randint(1, window_y-5),
            random.randint(1, window_x-5),
            random.randint(0, 3),
            random.choice(symbols),
        ))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


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
