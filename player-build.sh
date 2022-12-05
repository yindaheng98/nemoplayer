#!/bin/sh
./configure \
    --disable-vp8 \
    --enable-vp9 \
    --enable-libyuv \
    --target=x86_64-linux-gcc \
    --enable-debug \
    --log=yes \
    --enable-internal-stats \
    --disable-unit-tests \
    --enable-tools \
    --disable-install-docs \
    --enable-install-srcs
