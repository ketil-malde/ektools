# Actions to take
from datetime import datetime

def checkdate(obj):
    if obj['timestamp'] > datetime(2050, 1, 1, 0, 0) or obj['timestamp'] < datetime(1975, 1, 1, 0, 0):
        print('Warning: date ', obj['timestamp'], ' looks unreasonable to me.')

def checkgps(obj):
    # For NMEA GPS datagrams, check that timestamp matches GPS time
    return None

def rawinfo(obj):
    if obj['type'][:3] == b'RAW':
        print('some info about RAW objects here')
        
