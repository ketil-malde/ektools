#!/usr/bin/python3

from ektools import parse, index

import datetime
import hashlib
import mmap
import pynmea2 as nm

def genmeta(f):
    with open(f, "rb") as fh:
        with mmap.mmap(fh.fileno(), length=0, access=mmap.ACCESS_READ) as mf:
            sha1 = hashlib.sha1(mf)

    filename = f
    sha1sum = sha1.hexdigest()

    rcounts = {}
    nmea = {}
    survey_name = None
    startpos = None
    endpos = None
    timedeltas = []
    speeds = []
    starttime = None
    endtime = None
    heaves = []
    rolls = []
    pitch = []

    for pos, typ, ln, bstr in index(f):
        obj = parse(bstr)
        if starttime is None:
            starttime = obj['timestamp']
        endtime = obj['timestamp']  # last time standing

        if typ == 'CON0':
            for tspname in obj['configuration']:
                tsp = obj['configuration'][tspname]
                fq = int(tsp['frequency'])
                rcounts[fq] = { 'transducer': tspname, 'pings': 0, 'ranges': [] }
                if survey_name is None:
                    survey_name = tsp['survey_name']
                else:
                    assert survey_name == tsp['survey_name']

        elif typ == 'NME0':
            msg = nm.parse(obj['nmea_string'])
            msg_t = msg.sentence_type
            if msg_t == 'GGA':
                if startpos is None:
                    startpos = (msg.latitude, msg.longitude)
                endpos = (msg.latitude, msg.longitude)
            elif msg_t == 'VTG':
                speeds.append(float(msg.spd_over_grnd_kts))
            elif msg_t == 'ZDA':
                dt = obj['timestamp']
                t = msg.timestamp
                gps_t = datetime.datetime(msg.year, msg.month, msg.day,
                            t.hour, t.minute, t.second, t.microsecond)
                timedeltas.append((dt-gps_t).total_seconds())
            # collect start point, end point, average speed, clock error/offset

        elif typ == 'RAW0':
            fq = obj['frequency']
            rc = rcounts[fq]
            rc['pings'] = rc['pings']+1
            rng = round(len(obj['power'])*obj['sample_interval']*obj['sound_velocity'])
            if rng not in rc['ranges']:
                rc['ranges'].append(rng)
            heaves.append(obj['heave'])
            rolls.append(obj['roll'])
            pitch.append(obj['pitch'])

    def minavgmax(ls):
        return (min(ls), sum(ls)/len(ls), max(ls))

    return { 'filename': filename, 'sha1sum': sha1sum,
             'survey': survey_name.decode('latin-1'),
             'transponders': rcounts,
             'start_time': starttime, 'end_time': endtime,
             'start_position': startpos, 'end_position' : endpos,
             'vessel_speed': minavgmax(speeds),
             'heave': minavgmax(heaves), 'roll': minavgmax(rolls),
             'pitch': minavgmax(pitch),
             'clock_error' : minavgmax(timedeltas)
    }

if __name__ == '__main__':

    import argparse
    from actions import showdict

    p = argparse.ArgumentParser(description='Generate metadata from Simrad RAW files.')
    # p.add_argument()
    p.add_argument('FILE', nargs='+', help='input files in RAW format.')
    args = p.parse_args()

    for f in args.FILE:
        showdict(genmeta(f))
