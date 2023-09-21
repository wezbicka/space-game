# space-game

Игра про космос

## Как запустить

Требуется Python версии 3.10 или выше:

```bash
python3 main.py
```

Рекомендуется запускать на линуксовой ОС, но на windows тоже работает.

Или запустите на [repl.it](https://replit.com/@PolinaVezhbitsk/SpaceGame#main.py)

## Функция `draw_frame`

Функция выводит на экран многострочный текст — кадр анимации. Пример использования:

```python3
frame = '''\
┌───┐
│ 1 │
└───┘'''

draw_frame(canvas, row, column, frame)
canvas.refresh()
```

От [window.addstr()](https://docs.python.org/3/library/curses.html#curses.window.addstr) она отличается тем, что
справляется с многострочным текстом и не вылетает с ошибкой когда текст не влезает в экран.

Функция `draw_frame` умеет не только рисовать кадры анимации, но и стирать их. Для этого используется аргумент `negative=True`:

```python3
frame1 = '''\
┌───┐
│ 1 │
└───┘'''

frame2 = '''\
┌───┐
│ 2 │
└───┘'''

draw_frame(canvas, row, column, frame1)
canvas.refresh()

time.sleep(1)

# стираем предыдущий кадр, прежде чем рисовать новый
draw_frame(canvas, row, column, frame1, negative=True)
draw_frame(canvas, row, column, frame2)
canvas.refresh()

time.sleep(1)
...
```

## Функция `get_frames`

Функция возвращает считанные из папки `spaceship` анимации корабля.Вы можете передать при вызове функции ваше название.
Чтобы этого избежать блокировки асинхронного кода и не заставлять ждать ответа от файловой системы из-за чтение из файла.
