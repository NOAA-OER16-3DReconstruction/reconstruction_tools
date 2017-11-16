#!/usr/bin/env python3

import logging
import PhotoScan
import glob
import os, os.path
import json
import re

import argparse


def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item):
      return item

def findChunk( doc, chunkName ):
    return find(lambda chunk: chunk.label == chunkName, doc.chunks)

def addToChunk( doc, chunkName, imagedir, doAlign ):

    changed = False

    print("Checking image directory %s" % imagedir )
    images = glob.glob( os.path.join(imagedir, "*.png") )

    print("Adding %d frames to chunk \"%s\" from %s" % (len(images), chunkName, imagedir) )

    chunk = findChunk( doc, chunkName )

    if not chunk:
        chunk = doc.addChunk()
        chunk.label = chunkName

    for camera in chunk.cameras:
        p = camera.photo.path

        logging.info("Existing chunk has file %s", p)

        idx = [os.path.basename(i) for i in images].index( os.path.basename(p) )
        if idx:
            del images[idx]
        else:
            logging.info("Image %s in project but not in image set, removing..." % p)
            changed = True
            chunk.remove(camera)

    ## All elements remaining in images are _not_ in the chunk
    if len(images) > 0:
        logging.info("Adding %d images to chunk ", len(images))
        changed = True
        chunk.addPhotos(images)

        if doAlign and changed:
            chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy)
            chunk.alignCameras()



parser = argparse.ArgumentParser(description='Image set to photoscan project')

# parser.add_argument('photoscan', help='Photoscan project (will be created if it doesn\'t exist)', default=False)
# parser.add_argument('set', help='Images set', default=False)

parser.add_argument('imageset', help='Imageset')

# parser.add_argument('input', nargs='?',
#                     help='Regions files to process',
#                     default=False)
#
# parser.add_argument('--force', dest='force', action='store_true', help='Force re-download of images')

parser.add_argument('--align', action='store_true', help='Do align all chunks')

# parser.add_argument('--save-project-as', dest='projectname', default='project.psx')

parser.add_argument('--log', metavar='level', default='INFO',
                    help='Logging level')

parser.add_argument('--default-chunk', default='default')


imagedir = 'images/'
default_chunk_name = 'default'

args = parser.parse_args()
logging.basicConfig( level=args.log.upper() )

projectdir = os.path.dirname( args.imageset )
photoscan_proj = os.path.join(projectdir, "project.psz")

## Load imageSet
f = open(args.imageset)
imageset = json.load(f)
f.close()


doc = PhotoScan.app.document
if os.path.isfile(photoscan_proj):
    doc.open(photoscan_proj)
else:
    logging.info("Starting new project %s", photoscan_proj)

# Scan existing images
photoscan_images = []
default_chunk = None


if 'Frames' in imageset and len(imageset['Frames'])>0:
    chunkdir = os.path.join(projectdir, imagedir)
    addToChunk( doc, default_chunk_name, chunkdir, doAlign = args.align  )

if 'Chunks' in imageset:
    for name,chunk in imageset['Chunks'].items():
        chunkdir = os.path.join(projectdir, name, imagedir)
        changed = addToChunk( doc, name, chunkdir, doAlign = args.align )




doc.save(path=photoscan_proj)








# imagedir  = os.path.join(args.project, 'images' )


#
# logging.info("Photoscan project is %s", photoscan_proj )
# # logging.info("Image set is %s", args.set)
# #
# # ## Read the image set file
# # imageSet = 0
# # with open(args.set) as f:
# #     imageSet = json.load(f)
# #
# # print(imageSet)
# # frames = imageSet['Frames']
# # image_pattern = imageSet['ImageName'] if 'ImageName' in imageSet else "image_%06d.png"
# # logging.info("Using image pattern \"%s\"", image_pattern)
# #
# # # set image directory
# # image_dir = args.imagedir if args.imagedir else os.path.dirname(args.set)
# # logging.info("Using image directory %s", image_dir)
#
#
# logging.info("Photoscan %s activated", "is" if PhotoScan.app.activated else "is not")
#
# ## And open project
