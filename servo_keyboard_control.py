class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class ServoKeyboardControl:
    def __init__(self):
        self.getch = _Getch()
        self.sensitivity = 50

    #TODO: change print values to setTargetPosition

    #TODO: change method of sensitivity change for better precision
    
    def keyboard_control(self):
        while True:
            key = self.getch()

            # WASD Directional Controls
            if key == b'w':             #UP
                print('UP')
            elif key == b'a':           #LEFT
                print('LEFT')
            elif key == b's':           #DOWN
                print('DOWN')
            elif key == b'd':           #RIGHT
                print('RIGHT')

            # Arrow Key Directional Controls
            elif key == b'\x00':
                key = self.getch()
                if key == b'H':         #UP
                    print('UP')
                elif key == b'K':       #LEFT
                    print('LEFT')
                elif key == b'P':       #DOWN
                    print('DOWN')
                elif key == b'M':       #RIGHT
                    print('RIGHT')

            # Sensitivity Controls
            elif key == b'x':
                if self.sensitivity < 100:
                    self.sensitivity += 10
                    print(self.sensitivity)
                else:
                    print("max interval reached")
            elif key == b'z':
                if self.sensitivity > 10:
                    self.sensitivity -= 10
                    print(self.sensitivity)
                else:
                    print("min interval reached")
                
            elif key == b'q':
                break
            else:
                print(key, end=' ')


def main():
    controller = ServoKeyboardControl()
    controller.keyboard_control()

if __name__ == '__main__':
    main()