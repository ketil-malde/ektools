import struct
from util.ektools import index, parse
import sys
import os.path

fn = sys.argv[1]

idx = index(fn)

config = parse(idx[0][3])

assert config['subtype'] == 'configuration'
freqs = config['configuration'].keys()

def matches(ch,msg):
    p = parse(msg)
    if 'channel_id' in p.keys():
        return p['channel_id'].decode() == ch
    elif 'parameter' in p.keys():
        return p['parameter']['channel_id'] == ch
    else:
        return True

def dgram_write(f, dgram):
    """Write a datagram to a file"""
            hdr = struct.pack('<l',len(dgram))
            f.write(hdr)
            f.write(dgram)
            f.write(hdr)

def edit_xml(ch, xmlstr):
    """Remove all except channel ch from XML configuration"""
    # remove all channels not matching ch
    # remove empty <Transceiver> elements
    pass
            
split = {}
for a in freqs:
    split[a] = [(p,t,l,m) for p,t,l,m in index(fn) if matches(a,m)]

for a in freqs:
    print(f'Freq {a}, count: {len(split[a])}')
    counts = {}
    for x in split[a]:
        if x[1] not in counts:
            counts[x[1]] = 1
        else:
            counts[x[1]]+=1
    print(counts)
    outname = os.path.splitext(os.path.basename(fn))[0]+'_'+a+'.raw'
    with open(outname, 'wb') as f:
        for (pos,typ,length,dgram) in split[a]:
            # write length (dgram already contains type)
            dgram_write(f,dgram)
        
    
