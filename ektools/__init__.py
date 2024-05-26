import sys
import struct
import mmap

from ektools.date_conversion import nt_to_unix

# text colors: GREEN = '\033[92m', BLUE = '\033[94m', HEADER = '\033[95m', CYAN = '\033[96m', BOLD = '\033[1m', UNDERLINE = '\033[4m'
#              CLEAR = '\033[0m', YELLOW = '\033[93m', RED = '\033[91m'

def warn(*args, **kwargs):
    print('\033[93mWarning\033[0m', *args, file=sys.stderr, **kwargs)

def error(*args, **kwargs):
    print('\033[91mError:\033[0m', *args, file=sys.stderr, **kwargs)

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
    return p.from_string(str, len(str))

def index(f, maxcount=None):
    '''Build an index of datagrams in a Simrad RAW file.  This is a list of position, type, length, and (unparsed) contents.'''
    idx = []
    with open(f, "rb") as fh:
        with mmap.mmap(fh.fileno(), length=0, access=mmap.ACCESS_READ) as mf:
            pos = 0
            count = 0
            while pos < len(mf) and (maxcount is None or count < maxcount):
                l, m = struct.unpack('<l4s', mf[pos:pos + 8])
                if pos + l > len(mf):
                    raise Exception('Premature EOF, truncated RAW file?')
                v = struct.unpack('<l', mf[pos + l + 4:pos + l + 8])
                t = m.decode('latin-1')
                if v[0] != l: warn(f'Datagram at {pos}: control lenght mismatch ({l} vs {v[0]}) - endianness error or corrupt file?')
                idx.append((pos, t, l, mf[pos + 4:pos + 4 + l]))
                pos += l + 8
                count += 1
    return idx

# Support for d in ekfile('D2022012345.raw').dgrams():
class ekfile():
    def __init__(self, filename):
        self.fname = filename

    def datagrams(self):
        return ekfile_iterator(self.fname)

class ekfile_iterator():
    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        if self.fname == '-':
            self.fhandle = sys.stdin.buffer
        else:
            self.fhandle = open(self.fname, 'rb')
        return self

    def __next__(self):
        try:
            dg = self.read_dgram(self.fhandle)
        except struct.error:
            raise StopIteration
        return dg

    def read_dgram(self, fh):
        # read two longs
        buf = fh.read(4)
        length = struct.unpack('<l', buf)[0]
        msg = fh.read(length)
        msgtype = struct.unpack('4s', msg[:4])[0].decode('latin1')
        # Are we certain there is always a date stamp here?
        ntdate = struct.unpack('<2l', msg[4:12])
        buf = fh.read(4)
        v = struct.unpack('<l', buf)
        if v[0] != length: warn(f'Datagram control lenght mismatch ({length} vs {v[0]}) - endianness error or corrupt file?')
        return (msgtype, length, nt_to_unix(ntdate).replace(tzinfo=None), msg)
