"""
Title: pressingClicks
Description: This is a program to press clicks given an input routine and loops through.
Author: Marco A. Barreto - marcoagbarreto
Version: 17-Aug-2022
"""

try:
    from os import system as os_system, name as os_name
    from time import sleep as time_sleep
    from random import uniform as random_uniform
    from pynput.mouse import Controller, Button, Listener as mouseListener
    from pynput.keyboard import Key, Listener as keyboardListener
    from threading import Thread as threading_Thread
except ImportError as details:
    print("-E- Couldn't import module, try pip install 'module'")
    raise details

#  ======== settings ========
DELAY = 1.0  # in seconds
INTERVAL = 5.0  # in seconds
start_stop_key = Key.f12
exit_key = Key.esc
#  ==========================


def set_limits(point):
    """
    Sets random limits for a given point
    Parameters:
    @ point: type:int float, used for coordinates or time
    """
    if isinstance(point, float):
        limit = 0.2

    elif isinstance(point, int):
        limit = 2
    else:
        limit = 0
    upper = point + limit
    lower = point - limit
    return random_uniform(lower, upper)


class pressingClicks(threading_Thread):
    """
    pressingClicks
    """

    def __init__(self, delay, interval, stored_clicks):
        """
        Class initialization
        Parameters:
        @ delay: type:float, wait time between clicks
        @ interval: type:float, wait time between routines
        """
        super(pressingClicks, self).__init__()
        self.mouse = Controller()
        self.delay = delay
        self.interval = interval
        self.running = False
        self.program_running = True
        self.clicks = stored_clicks

    def click(self, xy):
        """
        Does the click action with left button
        Parameters:
        @ xy: type:tuple, x and y coordinates to click
        """
        time_sleep(set_limits(self.delay))
        # Set pointer position
        x = int(set_limits(xy[0]))
        y = int(set_limits(xy[1]))
        self.mouse.position = (x, y)
        # Press and release
        self.mouse.press(Button.left)
        time_sleep(random_uniform(0.1, 0.3))
        self.mouse.release(Button.left)

    def run(self):
        """
        Runs the clicks
        """
        while self.program_running:
            if self.running:
                for xy in self.clicks:
                    if self.running:
                        self.click(xy)
            time_sleep(set_limits(self.interval))

    def start_clicking(self):
        """
        Resumes the click action
        """
        self.running = True

    def stop_clicking(self):
        """
        Pauses the click action
        """
        self.running = False

    def exit(self):
        """
        Stops the program
        """
        self.stop_clicking()
        self.program_running = False


def display_controls():
    """
    Display Controls
    """
    print(' ----- Controls -------')
    print(' Left Button = Record Click')
    print(' Middle Button = Stop Recording')
    print(' F12 = Pause/Play')
    print(' Esc = Reset')
    print('-----------------------')


def set_delay_interval():
    """
    Input Delay and Interval Times
    """
    delay = input('Input the delay between clicks:')
    interval = input('Input interval between routines:')

    try:
        if delay.isdigit() > 0:
            delay = float(delay)
            print(f'Delay set to {delay}s')
    except TypeError:
        print('None numerical value entered.\nSetting delay default values.')
    finally:
        if isinstance(delay, float):
            pass
        else:
            delay = DELAY
            print(f'Delay default value loaded: {delay}s')

    try:
        if interval.isdigit() > 0:
            interval = float(interval)
            print(f'Interval set to {interval}s')
    except TypeError:
        print('None numerical value entered.\nSetting interval default values.')
    finally:
        if isinstance(interval, float):
            pass
        else:
            interval = INTERVAL
            print(f'Interval default value loaded: {interval}s')

    return delay, interval


def init_mouse():
    """
    Record Mouse Clicks
    """
    stored_clicks = []

    def on_click(x, y, button, pressed):
        """
        Used to record mouse clicks
        Parameters:
        @ x: type:int, x coordinate in screen
        @ y: type:int, y coordinate in screen
        @ button: type:class Button, mouse buttons
        @ pressed: type:bool, True if a button is pressed
        """
        if button == Button.middle:
            # Stop mouse listener
            print('Saving Clicks Routine')
            return False

        if pressed:
            print('Click', x, y)
            stored_clicks.append((x, y))

    mouse_listener = mouseListener(on_click=on_click)
    mouse_listener.start()
    print('Start Recording Clicks')
    mouse_listener.join()

    return stored_clicks


def init_keyboard(clicks):
    """
    Initialize Keyboard For Controls
    """

    def on_press(key):
        """
        Controller for pressingClicks,
        if a supported key is pressed,
        an action is raised.
        Parameters:
        @ key: type: Class keyboard, keyboard key
        """
        if key == start_stop_key:
            if clicks.running:
                print('Paused')
                clicks.stop_clicking()
            else:
                print('Play')
                clicks.start_clicking()

        elif key == exit_key:
            # Stop listener
            print('Program Stopped.')
            clicks.exit()
            return False

    keyboard_listener = keyboardListener(on_press=on_press)
    keyboard_listener.start()
    print('Press F12 To Start.')
    keyboard_listener.join()


def main():
    """
    pressingClicks is a program that allows to record clicks,
    add delay between clicks, intervals to loops and replay the clicks.
    """

    # Set terminal size to optimal size
    os_system('mode con cols=37 lines=15')

    # Set terminal to be always on top
    os_system('Powershell.exe -ExecutionPolicy UnRestricted -Command "(Add-Type -memberDefinition \\"[DllImport('
              '\\"\\"user32.dll\\"\\")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, '
              'int x,int y,int cx, int xy, uint flagsw);\\" -name \\"Win32SetWindowPos\\" -passThru )::SetWindowPos(('
              'Add-Type -memberDefinition \\"[DllImport(\\"\\"Kernel32.dll\\"\\")] public static extern IntPtr '
              'GetConsoleWindow();\\" -name \\"Win32GetConsoleWindow\\" -passThru )::GetConsoleWindow(),-1,0,0,0,0,'
              '67)"')

    # Clear the terminal after last command
    os_system('cls' if os_name == 'nt' else 'clear')

    while True:

        # Show the controls
        display_controls()

        # Input by user delay and interval times
        delay, interval = set_delay_interval()

        # Record click routine
        stored_clicks = init_mouse()

        # Run the program
        clicks = pressingClicks(delay, interval, stored_clicks)
        clicks.start()

        # Load controls
        init_keyboard(clicks)

        # Restart the program
        os_system('cls' if os_name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
