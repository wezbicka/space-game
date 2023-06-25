import time
import random
import asyncio

import curses


TIC_TIMEOUT = 0.1


def draw(canvas):
    symbols = '+*.:'
    canvas.border()
    window_y, window_x = canvas.getmaxyx()
    coroutines = []
    for i in range(100):
        coroutines.append(blink(
            canvas,
            random.randint(1, window_y-5),
            random.randint(1, window_x-5),
            random.choice(symbols),
        ))
    while True:
        for coroutine in coroutines.copy():
            curses.curs_set(False)
            try:
                coroutine.send(None)
                curses.curs_set(False)
            except StopIteration:
                coroutines.remove(coroutine)
            canvas.refresh()
        time.sleep(TIC_TIMEOUT)
    # time.sleep(2)

  
async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(3):
            await asyncio.sleep(0)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
