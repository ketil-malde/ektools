# Actions to take
from datetime import datetime
from output import warn, error

def checkdate():
    zeros = 0
    suspicious = 0
    def check(obj):
        nonlocal zeros
        nonlocal suspicious
        if obj is None:
            if zeros + suspicious > 0:
                warn(f'There were {zeros + suspicious} timestamp warnings:')
                warn(f'    Date fields of zero: {zeros}')
                warn(f'    Otherwise suspicious: {suspicious}')
        elif obj['low_date'] == 0 and obj['high_date'] == 0:
            warn(f'Datagram timestamp is zero.')
            zeros += 1
        elif obj['timestamp'] > datetime(2050, 1, 1, 0, 0) or obj['timestamp'] < datetime(1975, 1, 1, 0, 0):
            warn(f'Datagram timestamp {obj["timestamp"]} does not look reasonable.')
            suspicious += 1
    return check

def checkgps(obj):
    if obj is None: return
    # For NMEA GPS datagrams, check that timestamp matches GPS time
    return None

def showdict(obj, indent=4):
    if obj is None: return
    for k in obj.keys():
        if type(obj[k]) == type({}):
            showdict(obj[k], indent+4)
        else:
            print(indent*' ', k, repr(obj[k])[:72])

def rawinfo(obj):
    if obj is None: return
    if obj['type'][:3] == b'RAW':
        print('some info about RAW objects here')

def summarize():
    s = {}
    def sm(obj):
        if obj is None:
            print('Summary of contents:')
            showdict(s)
            return
        else:
            t = obj['type']
            if t in s.keys():
                s[t] += 1
            else:
                s[t] = 1
    return(sm)

# Filters

def filtertype(types):
    '''Given a list of types, return a filter that checks for matching type'''
    def f(p,t,l):
        return any(ty == t for ty in types)
    return f
        
