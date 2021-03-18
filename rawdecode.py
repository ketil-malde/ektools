#!/usr/bin/python3

import pickle
import sys

def unpickle_iter():
    try:
        while True:
             yield pickle.load(sys.stdin.buffer)
    except EOFError:
        # raise StopIteration
        return

for r in unpickle_iter():
    for dt,fs in r.items():
        print(dt,fs.keys())
        for f in fs:
            # print(f, fs[f]['mru'])
            print(f)


