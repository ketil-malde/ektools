from lxml import etree

# Annotation types:
#   Layers...
#   Schools...
# Coordinate systems - heave compensation?

# Format notes:
# - timestamps are seconds since epoch as a float (!)
# - species IDs are four-digit(?) numbers, registered by frequency?
# - boundaries (vertical, curve) and connectors (what are these?)

# parse workfile contents
def read_workfile(f):
    with open(f, 'rb') as fp: txt = fp.read()
    e = etree.from_string(txt)
    # Process it


