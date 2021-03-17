#!/usr/bin/python3

# import cProfile

import util.actions as act
from util.ektools import warn, error, parse, index

def process(df, verbose=False, filters=[], actions=[]):
    '''Process an indexed Simrad RAW file by applying a set of actions'''
    count = 0
    for pos, t, l, bstr in df:
        if verbose:
            print(f'Datagram {count}:\t{pos}\t{l}\t{t}')
        count += 1
        if actions:
            if not filters or any(f(pos,t,l) for f in filters):
                obj = parse(bstr)
                for a in actions:
                    a(obj)
    # signal end
    for a in actions:
        a(None)

if __name__ == '__main__':

    import argparse

    p = argparse.ArgumentParser(description='Extract information from Simrad RAW files.')
    p.add_argument('-t', '--type',  default=[], action='append', help='only apply to given datagram types')
    p.add_argument('-l', '--list',  action='store_true', help='output datagram contents extensively')
    p.add_argument('-s', '--summarize', action='store_true', help='summarize datagrams')
    p.add_argument('-q', '--quiet', action='store_true', help='produce minimal output')
    p.add_argument('-c', '--check', action='store_true', help='check datagram contents for consistency')
    p.add_argument('-r', '--rawdump', action='store_true', help='dump pickled raw datagrams')
    p.add_argument('FILE', nargs='+', help='input files in RAW format.')
    args = p.parse_args()
    
    actions = []

    if args.list:
        if args.quiet:
            error('Please specify at most one of -l and -q')
            exit(-1)
        else:
            actions.append(act.showdict)
    if args.rawdump:
        actions = [act.rawdump()] # override previous
        args.quiet = True
        if args.list: warn("Ignoring '-l' because '-r' was specified.")

    fs = []
    if args.type: fs.append(act.filtertype(args.type))

    if args.check:     actions.append(act.checkdate())
    if args.summarize: actions.append(act.summarize())
    
    for f in args.FILE:
        # print(f)
        d = index(f)
        # cProfile.run("process(d, verbose=not args.quiet, actions=actions, filters=fs)")
        process(d, verbose=not args.quiet, actions=actions, filters=fs)
