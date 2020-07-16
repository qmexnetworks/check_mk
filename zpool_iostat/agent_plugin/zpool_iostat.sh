#!/bin/sh

echo "<<<zpool_iostat>>>"

for i in `zpool list -Ho name`; do zpool iostat $i 1 2 | tail -n 1; done