# snake_terminal.py
import curses # Works on macOS/Linux out of the box; on Windows install windows-curses once
import random
import time

# Controls:
#  - Arrow keys or WASD to move
#  - P to pause/resume
#  - Q to quit

def main(stdscr):
    curses.curs_set(0)                 # hide cursor
    stdscr.nodelay(True)               # non-blocking input
    stdscr.keypad(True)                # read arrows
    curses.noecho()
    curses.cbreak()

    # Colors (optional fallback if terminal lacks colors)
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # food
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # hud

    # Playfield size (inside a border)
    max_y, max_x = stdscr.getmaxyx()
    # ensure minimum size
    min_h, min_w = 18, 32
    if max_y < min_h or max_x < min_w:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Please enlarge your terminal to at least {min_w}x{min_h}.")
        stdscr.refresh()
        stdscr.getch()
        return

    height, width = max_y - 2, max_x - 2  # inner area without border

    # Initial snake (center, length 3, moving right)
    cy, cx = height // 2, width // 2
    snake = [(cy, cx - 1), (cy, cx), (cy, cx + 1)]
    direction = (0, 1)  # dy, dx

    def random_empty_cell():
        while True:
            y = random.randint(1, height - 2)
            x = random.randint(1, width - 2)
            if (y, x) not in snake:
                return (y, x)

    food = random_empty_cell()
    score = 0
    step_delay = 0.12   # seconds per step; speeds up over time
    paused = False
    last_move_time = time.time()

    def draw():
        stdscr.clear()
        # Border
        stdscr.border()

        # HUD
        hud = f" Score: {score}   Length: {len(snake)}   Speed: {max(1, int(1/step_delay))}/s  (P=pause, Q=quit) "
        if curses.has_colors():
            stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, max(1, (max_x - len(hud)) // 2), hud[:max_x-2])
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(3))

        # Food
        fy, fx = food
        if curses.has_colors():
            stdscr.attron(curses.color_pair(2))
        stdscr.addch(fy, fx, "@")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(2))

        # Snake
        if curses.has_colors():
            stdscr.attron(curses.color_pair(1))
        # head
        hy, hx = snake[-1]
        stdscr.addch(hy, hx, "O")
        # body
        for y, x in snake[:-1]:
            stdscr.addch(y, x, "o")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(1))

        if paused:
            msg = " PAUSED "
            stdscr.addstr(max_y//2, max(1, (max_x - len(msg)) // 2), msg)

        stdscr.refresh()

    def set_direction(key, current):
        dy, dx = current
        # map keys -> directions, disallow direct 180° turns
        mapping = {
            curses.KEY_UP:    (-1, 0),
            curses.KEY_DOWN:  (1, 0),
            curses.KEY_LEFT:  (0, -1),
            curses.KEY_RIGHT: (0, 1),
            ord('w'): (-1, 0),
            ord('s'): (1, 0),
            ord('a'): (0, -1),
            ord('d'): (0, 1),
        }
        if key in mapping:
            ndy, ndx = mapping[key]
            if (ndy, ndx) != (-dy, -dx):  # prevent immediate reversal
                return (ndy, ndx)
        return current

    draw()

    while True:
        # Input
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            break
        if key in (ord('p'), ord('P')):
            paused = not paused
            draw()
            time.sleep(0.05)

        if not paused:
            # allow direction change even if not time to move yet
            direction = set_direction(key, direction)

        # Movement timing
        now = time.time()
        if paused or (now - last_move_time) < step_delay:
            time.sleep(0.01)
            continue
        last_move_time = now

        if paused:
            continue

        # Move snake
        dy, dx = direction
        hy, hx = snake[-1]
        ny, nx = hy + dy, hx + dx

        # Collision with walls (playable area is 1..height-2 and 1..width-2)
        if ny <= 0 or ny >= height - 0 or nx <= 0 or nx >= width - 0:
            break  # hit border

        # Collision with self
        if (ny, nx) in snake:
            break

        snake.append((ny, nx))

        # Eat food?
        if (ny, nx) == food:
            score += 1
            # speed up a bit every 3 foods (cap)
            if score % 3 == 0:
                step_delay = max(0.05, step_delay - 0.01)
            food = random_empty_cell()
            # don't pop tail -> snake grows
        else:
            # normal move: remove tail
            snake.pop(0)

        draw()

    # Game over screen
    stdscr.nodelay(False)
    msg1 = " GAME OVER "
    msg2 = f" Final score: {score}   Length: {len(snake)} "
    msg3 = " Press R to restart or any other key to quit "
    stdscr.addstr(max_y//2 - 1, max(1, (max_x - len(msg1)) // 2), msg1)
    stdscr.addstr(max_y//2,     max(1, (max_x - len(msg2)) // 2), msg2)
    stdscr.addstr(max_y//2 + 1, max(1, (max_x - len(msg3)) // 2), msg3)
    stdscr.refresh()
    k = stdscr.getch()
    if k in (ord('r'), ord('R')):
        main(stdscr)  # restart

if __name__ == "__main__":
    curses.wrapper(main)
