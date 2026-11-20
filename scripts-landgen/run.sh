#!/bin/sh
# Usage: sh /home/claude/me/landgen/run.sh <land dir>   builds vectors, terrain, sepia image and the labelled preview
set -e; G=/home/claude/me/landgen; L=$1
python3 $G/make_vectors.py $L && python3 $G/terrain.py $L && python3 /home/claude/me/scripts/regrade.py $L/data && python3 $G/preview.py $L
