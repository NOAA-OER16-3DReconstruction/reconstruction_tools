#!/bin/sh

PHOTOSCAN="/Applications/Photoscan/PhotoScanPro.app/Contents/MacOS/PhotoScanPro"

${PHOTOSCAN} -r scripts/photoscan.py $@
