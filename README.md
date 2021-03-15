Ektools is a small collection of utilities/library functions to work
with EK60 echo sounder data.  There are two executable programs which
take a RAW file as their parameter:

- ekplot.py - simple plot of the raw data from each channel
- eklist.py - extracts various information from the RAW file

# Examples

List an index of the datagrams in `file.raw`:

    eklist file.raw

Parse datagrams and print the contents of each (only truncate large
arrays):

    eklist -l file.raw
	
Check contents of the file for consistency (`-c`), while suppressing
other output (`-q`):

	eklist -qc file.raw

# Structure

The `eklist` program mainly parses the input and processes it with a
user-selected set of functions, defined in `actions.py`.  Of
particular interest is the function `type3_convert()`, which converts
from the native RAW format, to standard /sv/ values.

The parsers for individual datagram is taken from PyEchoLab, and can
be found in the `util` subdirectory.
