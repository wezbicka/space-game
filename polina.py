import time
import curses


def draw(canvas):
    canvas.border() # canvas.refresh()
    
    row, column = (5, 20)
    while True:
        canvas.addstr(row, column, '*', curses.A_DIM)
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(2)
        canvas.addstr(row, column, '*')
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(0.3)
        canvas.addstr(row, column, '*', curses.A_BOLD)
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(0.5)
        canvas.addstr(row, column, '*')
        curses.curs_set(False)
        canvas.refresh()
        time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
