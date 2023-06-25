import time
import curses
import random

def draw(canvas):
    
    stars = []
    x = curses.LINES
    y = curses.COLS
    for i in range(10):
        star_x = random.randint(1, x)
        star_y = random.randint(1, y)
        kord = (star_x, star_y)
        stars.append(kord)

    canvas.border()
    delay = (2, 0.3, 0.5, 0.3)
    count = 0
    while True:
        
        for i in stars:
            
            if count % 4 == 0:
                canvas.addstr(i[0], i[1], '*', curses.A_DIM)
            elif count % 4 == 2:
                canvas.addstr(i[0], i[1], '*', curses.A_BOLD)
            else:
                canvas.addstr(i[0], i[1], '*',)
        curses.curs_set(False)       
        count += 1
        canvas.refresh()
        time.sleep(delay[count % 4])

  
if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
