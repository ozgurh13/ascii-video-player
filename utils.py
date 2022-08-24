
import sys

def die(error_msg: str):
    '''
    print error message to stderr and exit program
    '''
    print(error_msg, file = sys.stderr, flush = True)
    exit(1)

