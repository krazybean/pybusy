import os
import sys
import json
import cursor
import logging
from time import sleep

from typing import NewType, List

# Logging of sorts
log = logging.getLogger(__name__)
hdlr = logging.StreamHandler(sys.stdout)
log.addHandler(hdlr)

# Type management for cleanliness
Frames = NewType('Frames', List[str])

# References from cli-spinners
JSON_SPINNERS = os.path.join('spinners', 'spinners.json')
spinners = json.loads(open(JSON_SPINNERS, 'r').read())


# Checking for ansicolors, cause fun...
try:
    from colors import color as hue
except ImportError:
    log.error('ansicolors not installed')

def setup(frames: Frames) -> str:
    while True:
        for cursor in frames:
            yield cursor

emoji_keys = ['arrow2','smiley', 'monkey', 'hearts', 'clock', 'earth', 'moon',
              'runner', 'weather', 'christmas']

def animate(name: str, loop: int=0, color: str=None) -> object:
    """
    Simple animation functionality wrapped around cli-spinner json file

    Usage: `cursors.animate('hamburger', loop=10000, color='yellow')
    Usage: `cursors.animate('dots3')

    Args:
        name (str): Name of the spinner key (can be obtained from cursor_list
        loop (int): Optional, number of iterations to run, or 0 == forever
        color (str): Optional, ansi color name using lib(ansicolors)
    Returns:
        None: Response is sys.stdout.write() to bash terminal
    """
    if name not in spinners.keys():
        return log.error(f"No cursor found for: {name}")
    if name in emoji_keys:
        unsupported = f'{name} not yet supported'
        return log.error(f"{unsupported}")
    interval = spinners[name].get('interval')
    frames = spinners[name].get('frames')
    setup_frames = setup(frames)
    loop_count = 0
    color = 'default' if not color else color
    while True:  # Outer-loop
        try:
            for _ in range(len(frames)):  # Inner-loop (by frame duration
                # sys.stdout.write("\033[?25l")  # Hides active blinking cursor
                cursor.hide()
                sys.stdout.write(hue(setup_frames.__next__(), fg=color))
                sys.stdout.flush()
                sleep(interval*0.001)
                sys.stdout.write('\b\r')
            loop_count += 1
            if loop > 0 and loop_count >= loop:
                break
        except KeyboardInterrupt:
            break
        except ValueError as e:
            log.error(f"{e}")
            break;
        finally:
            cursor.show()

def cursor_list() -> List:
    """
    List of all available cursor styles

    Usage: `cursors.cursor_list()`

    Args:
        None: No argument needed for initiation
    Returns:
        spinners (list): List of available cursor/spinners
    """
    return [item for item in spinners.keys() if item not in emoji_keys]


if __name__ == '__main__':
    # Demo
    # for cursor in cursor_list():
    #     print(cursor)
    #     animate(cursor, color='yellow', loop=3)
    # print(cursor_list())  # Obtain List
    animate('dots4')  # Action command
