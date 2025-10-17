import sys
import os

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif '__file__' in globals():
        return os.path.dirname(os.path.abspath(__file__))
    else:
        return os.path.dirname(os.path.realpath(sys.argv[0]))

