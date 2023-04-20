#!/bin/bash
FRAME=$1 # 剪多少帧
HEADER="video,start"
for ((F = 0; F < $FRAME; F++)); do
    HEADER="$HEADER,$F"
done
echo $HEADER
