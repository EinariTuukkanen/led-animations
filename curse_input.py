
import curses

def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    c2 = -1
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c2 != -1 and c == -1:
            print('test')
        if c != -1:
            # print numeric value
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)
            print(c)

if __name__ == '__main__':
    curses.wrapper(main)