# Actions to take
from datetime import datetime
from ektools import warn, error

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
            print(indent*' ',k,'{')
            showdict(obj[k], indent+4)
            print(indent*' ','}')
        else:
            print(indent*' ', k, repr(obj[k])[:72])

def rawinfo():
    config = {}
    def ri(obj):
        print('RI', obj['type'])
        if obj is None:
            return
        elif obj['type'] == 'CON0':
            # store config for each channel by frequency
            cf = obj['configuration']
            for transp in cf:
                tcf = cf[transp]
                config[tcf['frequency']] = tcf
        elif obj['type'][:3] == 'RAW':
            print('Power: ', obj['power'])
            print('s_v:   ', type3_convert(config[obj['frequency']], obj))
    return ri

from conversion import calc_sv

def type3_convert(cnf, obj):
    '''Converting raw power to s_v using Type 3 definition from the NetCDF standard'''
    return calc_sv(
        P_c             = obj['power'],                   # vector of power received
        alpha           = obj['absorption_coefficient'],  # acoustic attenuation
        pt              = obj['transmit_power'],          # transducer power
        sound_vel       = obj['sound_velocity'],          # speed of sound
        wavelen         = obj['sound_velocity'] / obj['frequency'],  # wavelength
        transducer_gain = cnf['gain'],                    # G0 in Type 3.
        sample_interval = obj['sample_interval'],         # transducer sampling rate
        eq_beam_angle   = cnf['equivalent_beam_angle'],   # ?
        pulse_length    = obj['pulse_length'],            # lenght of each ping
        sa_corr         = -0.57     # FIXME: cnf['sa_correction_table'] , but it is an array, which element to use?
    )

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
        
