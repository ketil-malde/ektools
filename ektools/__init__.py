import sys
import struct
import mmap

# text colors: GREEN = '\033[92m', BLUE = '\033[94m', HEADER = '\033[95m', CYAN = '\033[96m', BOLD = '\033[1m', UNDERLINE = '\033[4m'
#              CLEAR = '\033[0m', YELLOW = '\033[93m', RED = '\033[91m'

def warn(*args, **kwargs):
    print('\033[93mWarning\033[0m',*args, file=sys.stderr, **kwargs)

def error(*args, **kwargs):
    print('\033[91mError:\033[0m',*args, file=sys.stderr, **kwargs)

import ektools.simrad_parsers as sp
import ektools.korona_parsers as kp

def parse(str):
    '''Table for selecting the correct parser to use for datagrams.
       Throws an exception if the datagram isn't known.'''
    # duplicates the simrad_raw_file.DGRAM_TYPE_KEY, but with bytestring keys
    parsers = {
          b'BOT' : sp.SimradBottomParser()
        , b'CON' : sp.SimradConfigParser()
        , b'DEP' : sp.SimradDepthParser()
        , b'FIL' : sp.SimradFILParser()
        , b'MRU' : sp.SimradMRUParser()
        , b'NME' : sp.SimradNMEAParser()
        , b'RAW' : sp.SimradRawParser()
        , b'TAG' : sp.SimradAnnotationParser()
        , b'XML' : sp.SimradXMLParser()
        , b'IDX' : sp.SimradIDXParser()

        , b'TNF' : kp.SimradTrackInfoParser()
        , b'TBR' : kp.SimradTrackBorderParser()
        , b'TTC' : kp.SimradTrackContentsParser()
    }

    dgram_type = str[:3]
    p = parsers[dgram_type]
    return(p.from_string(str, len(str)))

def index(f):
    '''Build an index of datagrams in a Simrad RAW file.  This is a list of position, type, length, and (unparsed) contents.'''
    idx = []
    with open(f, "rb") as fh:
        with mmap.mmap(fh.fileno(), length=0, access=mmap.ACCESS_READ) as mf:
            pos = 0
            while pos < len(mf):
                l, m = struct.unpack('<l4s', mf[pos:pos+8])
                if pos+l > len(mf):
                    raise Exception('Premature EOF, truncated RAW file?')
                v = struct.unpack('<l', mf[pos+l+4:pos+l+8])
                t = m.decode('latin-1')
                if v[0]!=l: warn(f'Datagram at {pos}: control lenght mismatch ({l} vs {v[0]}) - endianness error or corrupt file?')
                idx.append((pos,t,l,mf[pos+4:pos+4+l]))
                pos += l+8
    return idx
    
