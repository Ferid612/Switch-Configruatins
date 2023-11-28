import tty
import sys
import termios

def get_key():
    tty.setcbreak(sys.stdin)
    try:
        key = sys.stdin.read(1)
        return key
    finally:
        restore_terminal()
        
        
# Save original terminal settings
original_settings = termios.tcgetattr(sys.stdin)

def restore_terminal():
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_settings)

# while True:
#     key = get_key()
#     print(f"You pressed: {key}")
#     if key == '\x1b':  # Exit loop if 'Esc' key is pressed
#         break