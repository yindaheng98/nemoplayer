#!/bin/sh -x
DOSCALE="$(dirname $0)/scale_down.sh"
ORIGIDIR=$1
SMALLDIR=$2
SCALE=4
for ORIGIPATH in "$ORIGIDIR"/*; do
    SMALLPATH="$SMALLDIR/$(basename $ORIGIPATH)"
    mkdir -p "$SMALLDIR"
    "$DOSCALE" "$ORIGIPATH" "$SMALLPATH" "$SCALE"
done
