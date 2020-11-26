# class bcolors:
    # FAIL = 
    # OKGREEN = '\033[92m'
    # WARNING = 
    # OKBLUE = '\033[94m'
    # HEADER = '\033[95m'
    # OKCYAN = '\033[96m'
    # ENDC = 
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'

import sys

def warn(*args, **kwargs):
    print('\033[93mWarning\033[0m',*args, file=sys.stderr, **kwargs)

def error(*args, **kwargs):
    print('\033[91mError:\033[0m',*args, file=sys.stderr, **kwargs)
