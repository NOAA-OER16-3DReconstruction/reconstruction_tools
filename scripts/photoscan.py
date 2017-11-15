#!/usr/bin/env python3

import logging
import PhotoScan
import glob
import os, os.path
import json
import re

import argparse


parser = argparse.ArgumentParser(description='Image set to photoscan project')

# parser.add_argument('photoscan', help='Photoscan project (will be created if it doesn\'t exist)', default=False)
# parser.add_argument('set', help='Images set', default=False)

parser.add_argument('project', help='Project directory')

# parser.add_argument('input', nargs='?',
#                     help='Regions files to process',
#                     default=False)
#
# parser.add_argument('--force', dest='force', action='store_true', help='Force re-download of images')

parser.add_argument('--align', action='store_true', help='Do align all chunks')

# parser.add_argument('--save-project-as', dest='projectname', default='project.psx')

parser.add_argument('--log', metavar='level', default='INFO',
                    help='Logging level')

parser.add_argument('--chunk', default='default')

# parser.add_argument('--input', nargs='?', default='images/', help='Working directory')
#
# parser.add_argument('--image-size', dest='imgsize', nargs='?', default='320x240')

# parser.add_argument('--with-groundtruth', dest='groundtruth', action='store_true')
#
# parser.add_argument("--ground-truth", dest="groundtruthfile",
#                     default="classification/ground_truth.json")
#
# parser.add_argument("--image-format", dest="imageext", default='jpg')
#
# parser.add_argument('--lazycache-url', dest='lazycache', default=os.environ.get("LAZYCACHE_URL", None),
#                     help='URL to Lazycache repo server (only needed if classifying)')

args = parser.parse_args()
logging.basicConfig( level=args.log.upper() )

photoscan_proj = os.path.join(args.project, "project.psz")
imagedir  = os.path.join(args.project, 'images' )

images = glob.glob( os.path.join(imagedir, "*.png") )
logging.info("Checking %d images", len(images))
image_basenames = [os.path.basename(i) for i in images]

logging.info("Photoscan project is %s", photoscan_proj )
# logging.info("Image set is %s", args.set)
#
# ## Read the image set file
# imageSet = 0
# with open(args.set) as f:
#     imageSet = json.load(f)
#
# print(imageSet)
# frames = imageSet['Frames']
# image_pattern = imageSet['ImageName'] if 'ImageName' in imageSet else "image_%06d.png"
# logging.info("Using image pattern \"%s\"", image_pattern)
#
# # set image directory
# image_dir = args.imagedir if args.imagedir else os.path.dirname(args.set)
# logging.info("Using image directory %s", image_dir)


logging.info("Photoscan %s activated", "is" if PhotoScan.app.activated else "is not")

## And open project
doc = PhotoScan.app.document
if os.path.isfile(photoscan_proj):
    doc.open(photoscan_proj)
else:
    logging.info("Starting new project %s", photoscan_proj)

# Scan existing images
photoscan_images = []
default_chunk = None

for chunk in doc.chunks:

    if chunk.label == args.chunk:
        default_chunk = chunk

    for camera in chunk.cameras:
        p = camera.photo.path

        logging.info("Existing chunk has file %s", p)

        if os.path.basename(p) not in image_basenames:
            logging.info("Image %s in project but not in image set, removing...")
            chunk.remove(camera)
        else:
            photoscan_images.append(os.path.basename(p))

for i in images:
    if os.path.basename(i) not in photoscan_images:
        logging.info("Adding image %s to project in chunk %s", i, args.chunk)

        if not default_chunk:
            logging.info("Needed to create chunk %s", args.chunk)
            default_chunk = doc.addChunk()
            default_chunk.label = args.chunk

        default_chunk.addPhotos([i])


if args.align:
    for chunk in doc.chunks:
        chunk.alignCameras()

doc.save(path=photoscan_proj)
