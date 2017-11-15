#!/bin/sh

#PHOTOSCAN="/Applications/Photoscan/PhotoScanPro.app/Contents/MacOS/PhotoScanPro"
PHOTOSCAN="/opt/photoscan-pro/photoscan.sh"

${PHOTOSCAN} -r scripts/photoscan.py $@
