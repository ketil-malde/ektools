#!/bin/bash

set -e

TESTFILE=D20180303-T093354.raw

if test ! -e $TESTFILE; then
    echo "Downloading test data: $TESTFILE"
    curl https://malde.org/~ketil/D20180303-T093354.raw -o D20180303-T093354.raw
fi

echo -n "Testing: tools/eklist..."
test "$(tools/eklist D20180303-T093354.raw | sha1sum | cut -f1 -d' ')" = "1a6c50e21289e5083c341fefa9f2dd0a75ce4898" && echo "OK" || echo "Failed"

echo -n "Testing: tools/eklist -l..."
test "$(tools/eklist -l D20180303-T093354.raw | sha1sum | cut -f1 -d' ')" = "1a6c50e21289e5083c341fefa9f2dd0a75ce4898" && echo "OK" || echo "Failed"
