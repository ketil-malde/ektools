#/usr/bin/python3

import pickle
import sys

def unpickle_iter():
    try:
        while True:
             yield pickle.load(sys.stdin.buffer)
    except EOFError:
        raise StopIteration

for r in unpickle_iter():    
    print(r.keys())

