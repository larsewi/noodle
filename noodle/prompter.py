from unicurses import *
import string
from utils import NOODLE_HEADER

KEY_CODE_DEL = 127
KEY_CODE_ENT = 10
KEY_CODE_EOF = 4
KEY_CODE_ESC = 27


def select(prompt, choices):
    try:
        stdscr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(stdscr, True)

        highlight = 0
        filter = ""
        filtered = list(choices)
        choice = None

        while True:
            # Draw menu
            clear()
            offset = 0
            for line in NOODLE_HEADER.splitlines():
                mvaddstr(offset, 0, line)
                offset += 1
            mvaddstr(
                offset, 0, f"{prompt} {filter} [Use arrows to move, type to filter]"
            )
            offset += 1
            for i in range(len(filtered)):
                if highlight == i:
                    attron(A_REVERSE)
                    mvaddstr(offset, 0, "> %s" % filtered[i])
                    attroff(A_REVERSE)
                else:
                    mvaddstr(offset, 0, "  %s" % filtered[i])
                offset += 1
            refresh()

            # Handle input
            ch = getch()
            if ch == KEY_UP and len(filtered) > 0:
                # Move highlight up
                highlight = (highlight - 1) % len(filtered)
            elif ch == KEY_DOWN and len(filtered) > 0:
                # Move highlight down
                highlight = (highlight + 1) % len(filtered)
            elif ch in (KEY_CODE_ENT, KEY_RIGHT):
                # Select highlighted
                if len(filtered) > 0:
                    choice = filtered[highlight]
                    break
            elif ch in (KEY_CODE_ESC, KEY_CODE_EOF, KEY_LEFT):
                # Cancel selection
                break
            elif chr(ch) in string.printable or ch == KEY_CODE_DEL:
                # Filter results
                filter = filter[:-1] if ch == KEY_CODE_DEL else filter + chr(ch)
                highlight = 0
                filtered = [c for c in choices if c.lower().startswith(filter.lower())]
    finally:
        endwin()

    return choice


def multi_select(prompt, choices, ticked=[]):
    try:
        stdscr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(stdscr, True)

        highlight = 0
        filter = ""

        selected = sorted(choice for choice in choices if choice in ticked)
        unselected = sorted(choice for choice in choices if choice not in ticked)
        filtered = selected + unselected

        while True:
            # Draw menu
            clear()
            offset = 0
            for line in NOODLE_HEADER.splitlines():
                mvaddstr(offset, 0, line)
                offset += 1
            mvaddstr(
                offset, 0, f"{prompt} {filter} [Use arrows to move, type to filter]"
            )
            offset += 1
            for i in range(len(filtered)):
                if highlight == i:
                    attron(A_REVERSE)
                choice = filtered[i]
                mvaddstr(offset, 0, f"[{'x' if choice in ticked else ' '}] {choice}")
                if highlight == i:
                    attroff(A_REVERSE)
                offset += 1
            refresh()

            # Handle input
            ch = getch()
            if ch == KEY_UP and len(filtered) > 0:
                # Move highlight up
                highlight = (highlight - 1) % len(filtered)
            elif ch == KEY_DOWN and len(filtered) > 0:
                # Move highlight down
                highlight = (highlight + 1) % len(filtered)
            elif ch in (KEY_CODE_ENT, KEY_RIGHT):
                # Select highlighted
                break
            elif ch in (KEY_CODE_ESC, KEY_CODE_EOF, KEY_LEFT):
                # Cancel selection
                return None
            elif chr(ch) in string.printable or ch == KEY_CODE_DEL:
                if chr(ch) == " " and len(filtered) > 0:
                    # Select
                    choice = filtered[highlight]
                    if choice in ticked:
                        ticked.remove(choice)
                    else:
                        ticked.append(choice)
                else:
                    # Filter results
                    filter = filter[:-1] if ch == KEY_CODE_DEL else filter + chr(ch)
                    highlight = 0

                    filtered = sorted(
                        c for c in choices if c.lower().startswith(filter.lower())
                    )
                    selected = sorted(choice for choice in filtered if choice in ticked)
                    unselected = sorted(
                        choice for choice in filtered if choice not in ticked
                    )
                    filtered = selected + unselected
    finally:
        endwin()

    return ticked


def file_picker(prompt, dir, include=None, exclude=None):
    entries = os.scandir(dir)
    dirs = []
    files = []
    for entry in entries:
        name = entry.name
        if entry.is_dir():
            dirs.append(f"{name}/")
            continue
        extension = os.path.splitext(name)[-1]
        if exclude and extension in exclude:
            continue
        if include and extension not in include:
            continue
        files.append(name)

    filename = select(prompt, sorted([".."] + dirs + files))
    if filename is None:
        return None
    path = os.path.join(dir, filename)
    if os.path.isdir(path):
        return file_picker(prompt, path)
    return path
