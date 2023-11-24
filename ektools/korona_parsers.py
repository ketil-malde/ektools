from .simrad_parsers import _SimradDatagramParser

"""
These parsers are similar to Simrad Parsers, but process datagrams 
found in RAW files after processing with the Korona library.

| Authors:
|       Ingrid Utseth <utseth@nr.no>
|       Ketil Malde <ketil@malde.org>

"""

class SimradTrackInfoParser(_SimradDatagramParser):
    '''
    Class for detecting and parsing TrackInfo datagrams from Korona tracking modules.
    Not a part of the pyecholab package.

    The track info datagram contains the following keys

        type:           string == 'TNF0'
        low_date:       long uint representing LSBytes of 64bit NT date
        high_date:      long uint representing MSBytes of 64bit NT date
        id:             long uint representing the ID of this track
        channel:        ushort representing the channel this track was detected on
        valid:          byte == 1 if track is valid, 0 otherwise
        pingSinceFirst: long uint representing the number of pings since the start of this track, relative to this ping
        pingSinceLast:  long uint representing the number of pings since the end of this track, relative to this ping
    '''
    def __init__(self):
        headers = {0: [('type', '4s'),  # TNF0
                       ('nttime_low', 'L'),  # NT time (low, high)
                       ('nttime_high', 'L'),  # NT time (low, high)
                       ('id', 'L'),  # ID of this track
                       ('channel', 'H'),  # The channel this track was detected on
                       ('valid', 'B'),  # 1 if this track is marked as valid, otherwise 0
                       ('pingsSinceFirst', 'L'),  # Number of pings since the start of this track, relative to this ping
                       ('pingsSinceLast', 'L'),]  # Number of pings since the end of this track, relative to this ping
                   }

        _SimradDatagramParser.__init__(self, "TNF", headers)

    def _unpack_contents(self, raw_string, length, version=0):
        assert self.header_size(0) == length, "Datagram length does not match format"

        header_values = struct.unpack(self.header_fmt(version), raw_string[:self.header_size(version)])
        data = {}

        for indx, field in enumerate(self.header_fields(version)):
            data[field] = header_values[indx]

        data['type'] = data['type'].decode('latin-1')
        data['timestamp'] = nt_to_unix((data['nttime_low'], data['nttime_high']))
        data['timestamp'] = data['timestamp'].replace(tzinfo=None)
        return data


class SimradTrackBorderParser(_SimradDatagramParser):
    '''
    Class for detecting and parsing TrackBorder datagrams from Korona tracking modules.
    Not a part of the pyecholab package.

    The track border datagram contains the following keys

        type:           string == 'TBR0'
        low_date:       long uint representing LSBytes of 64bit NT date
        high_date:      long uint representing MSBytes of 64bit NT date
        id:             long uint representing the ID of this track
        channel:        ushort representing the channel this track was detected on
        minDepth:       float representing the minimum depth of this track
        maxDepth:       float representing the maximum depth of this track
        peakDepth:      float representing the peak depth of this track
    '''
    def __init__(self):
        headers = {0: [('type', '4s'),  # TBR0
                       ('nttime_low', 'L'),  # NT time (low, high)
                       ('nttime_high', 'L'),  # NT time (low, high)
                       ('id', 'L'),  # ID of this track
                       ('channel', 'H'),  # The channel this track was detected on
                       ('minDepth', 'f'),  # [m]
                       ('maxDepth', 'f'),  # [m]
                       ('peakDepth', 'f')]  # [m]
                   }

        _SimradDatagramParser.__init__(self, "TBR", headers)

    def _unpack_contents(self, raw_string, length, version=0):
        assert self.header_size(0) == length, "Datagram length does not match format"

        header_values = struct.unpack(self.header_fmt(version), raw_string[:self.header_size(version)])
        data = {}

        for indx, field in enumerate(self.header_fields(version)):
            data[field] = header_values[indx]

        data['type'] = data['type'].decode('latin-1')
        data['timestamp'] = nt_to_unix((data['nttime_low'], data['nttime_high']))
        data['timestamp'] = data['timestamp'].replace(tzinfo=None)
        return data


class SimradTrackContentsParser(_SimradDatagramParser):
    '''
    Class for detecting and parsing Track Table of Contents datagram datagrams from Korona tracking modules.
    Not a part of the pyecholab package.

    The track contents datagram contains the following keys

        type:           string == 'TTC0'
        low_date:       long uint representing LSBytes of 64bit NT date
        high_date:      long uint representing MSBytes of 64bit NT date
        validCount:     long uint representing the number of valid tracks
        validIds:       array of long uints representing the ids of the valid tracks
        timesCount:     long uint representing the number of pings containing one or more Track info datagram
        pingTimes:      array of long uints representing the time of pings containing one or more Track info datagram
    '''
    def __init__(self):
        headers = {0: [('type', '4s'),  # TTC0
                       ('nttime_low', 'L'),  # NT time (low, high)
                       ('nttime_high', 'L'),  # NT time (low, high)
                       ('validCount', 'L')]  # The number of valid tracks
                   }

        _SimradDatagramParser.__init__(self, "TCO", headers)

    def _unpack_contents(self, raw_string, length, version=0):
        # assert self.header_size(0) == length, "Datagram length does not match format"

        header_values = struct.unpack(self.header_fmt(version), raw_string[:self.header_size(version)])
        data = {}

        for indx, field in enumerate(self.header_fields(version)):
            data[field] = header_values[indx]

        data['type'] = data['type'].decode('latin-1')
        data['timestamp'] = nt_to_unix((data['nttime_low'], data['nttime_high']))
        data['timestamp'] = data['timestamp'].replace(tzinfo=None)

        if data['validCount'] == 0:
            data['validIds'] = []
            data['timesCount'] = 0
            data['pingTimes'] = []
        else:
            # Get format string for the list of valid track ids
            _fmt_valid = '<' + 'L'*data['validCount'] #+ 'L' #+ 'L'*data['validCount']*2

            # Unpack the list of valid track ids
            pos = self.header_size(0)
            _values = struct.unpack(_fmt_valid,
                                    raw_string[pos:pos + struct.calcsize(_fmt_valid)])
            pos += struct.calcsize(_fmt_valid)
            data['validIds'] = list(_values)

            # Unpack the number of pings with one or more valid track
            _fmt_times_count = "<L"
            _values = struct.unpack(_fmt_times_count,
                                    raw_string[pos:pos + struct.calcsize(_fmt_times_count)])
            data['timesCount'] = _values[0]
            pos += struct.calcsize(_fmt_times_count)

            # Get format string for the list of ping times
            _fmt_ping_times = '<' + 'L'*data['timesCount']*2

            # Check that the total format string length matches the datagram length
            final_pos = pos + struct.calcsize(_fmt_ping_times)
            assert final_pos == length, "Datagram length does not match format"

            # Unpack the list of ping times
            _values = struct.unpack(_fmt_ping_times, raw_string[pos:length])

            # Convert list of NT times to list of unix times
            data['pingTimes'] = []
            idx = 0
            for _ in range(data['timesCount']):
                ping_time = nt_to_unix((_values[idx], _values[idx+1]))
                data['pingTimes'].append(ping_time.replace(tzinfo=None))
                idx += 2

        return data
