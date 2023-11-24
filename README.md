Ektools is a small collection of utilities/library functions to work
with Simrad EK60 and EK80 echo sounder data.  There are two executable
programs which take a RAW file as their parameter:

- ekplot - simple plot of the raw data from each channel
- eklist - extracts various information from the RAW file
- ekmeta - display metadata (times and locations, etc)
- eksplit - split a RAW file by configuration

The `ektools` library provides fast indexing functions, and parsers
(mostly taken from the `PyEchoLab` package) for the various datagrams
used by Simrad and the Korona processing package.

# Examples

List an index of the datagrams in `file.raw`:

    eklist file.raw

Parse datagrams and print the contents of each (only truncate large
arrays):

    eklist -l file.raw
	
Only print detailed information on specific datagrams (in this case,
MRU datagrams containing information on ship movement):

	eklist -ql -t MRU0 -t MRU1 file.raw

Check contents of the file for consistency (`-c`), while suppressing
other output (`-q`):

	eklist -qc file.raw

Dump normalized (converted to s_v and with corrected angles) RAW data
in a binary stream to stdout:

    eklist -qr file.raw
	
The `rawdecode.py` file demonstrates how to read the stream back in
again.

Extract metadata from a RAW file:

	ekmeta file.raw
	
Separate a RAW file into its different configurations:

	eksplit file.raw

