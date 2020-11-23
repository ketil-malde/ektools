# Actions to take
from datetime import datetime

def checkdate(obj):
    if obj is None: return
    if obj['timestamp'] > datetime(2050, 1, 1, 0, 0) or obj['timestamp'] < datetime(1975, 1, 1, 0, 0):
        print(f'Warning: datagram timestamp {obj["timestamp"]} looks unreasonable to me.')
        # print(obj)

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
        
