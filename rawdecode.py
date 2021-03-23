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

if __name__ == '__main__':
    for r in unpickle_iter():
        for datetime,freqs in r.items():
            print(datetime,freqs.keys())
            for f in freqs:
                # print(f, fs[f]['mru'])
                print(f)


