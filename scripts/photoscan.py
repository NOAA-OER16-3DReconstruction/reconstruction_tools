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

parser.add_arguments('project', help='Project directory')

# parser.add_argument('input', nargs='?',
#                     help='Regions files to process',
#                     default=False)
#
# parser.add_argument('--force', dest='force', action='store_true', help='Force re-download of images')

# parser.add_argument('--squash-runs', dest='squashruns', action='store_true', help='Squash runs of multiple identical tags')
#
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

photoscan = os.join(args.project)

logging.info("Photoscan project is %s", args.photoscan)
logging.info("Image set is %s", args.set)

## Read the image set file
imageSet = 0
with open(args.set) as f:
    imageSet = json.load(f)

print(imageSet)
frames = imageSet['Frames']
image_pattern = imageSet['ImageName'] if 'ImageName' in imageSet else "image_%06d.png"
logging.info("Using image pattern \"%s\"", image_pattern)

# set image directory
image_dir = args.imagedir if args.imagedir else os.path.dirname(args.set)
logging.info("Using image directory %s", image_dir)


logging.info("Photoscan %s activated", "is" if PhotoScan.app.activated else "is not")

## And open project
doc = PhotoScan.app.document
if os.path.isfile(args.photoscan):
    doc.open(args.photoscan)
else:
    logging.info("Starting new project %s", args.photoscan)

# Scan existing images
for chunk in doc.chunks:
    for camera in chunk.cameras:
        p = camera.image().path

        logging.info("Existing chunk has file %s", p)

doc.save(path=args.photoscan)


# ## Look for json file
# meta = False
# center_path = False
# json_file = args.input + "/images.json"
# if os.path.exists(json_file):
#     with open(json_file) as f:
#         meta = json.load(f)
#
#         ## Find the p0_z0 scene
#         center_tag_re = "p0_z0"
#         center_paths = next(v for k,v in meta.items() if re.search(center_tag_re,k))
#
#         center_paths = [os.path.basename(p) for p in center_paths]
#
#         print(center_paths)
#
#
# logging.info("Photoscan %s activated" % ("is" if PhotoScan.Application.activated else "is not"))
#
# doc = PhotoScan.app.document
# chunk = doc.addChunk()
# group = chunk.addCameraGroup()
# group.type = PhotoScan.CameraGroup.Station
#
# images = glob.glob(args.input + "/*")
#
# if len(images) == 0:
#     logging.warning("Found no images in %s" % args.input)
#     exit(-1)
#
# logging.info("Adding %d images" % len(images))
#
# chunk.addPhotos(images, PhotoScan.FlatLayout)
#
#
# ## Assign chunk to our station group
# for c in chunk.cameras:
#     c.group = group
#
#     if center_paths and os.path.basename(c.photo.path) in center_paths:
#         print("Found camera for center path at %s, fixing to the origin" % c.photo.path)
#
#         c.reference.rotation     = PhotoScan.Vector([0,0,0])
#         c.reference.accuracy_ypr = PhotoScan.Vector([5,5,5])
#
#
# chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, generic_preselection=True, reference_preselection=False)
# chunk.alignCameras()
#
# chunk.transform.rotation = PhotoScan.Utils.ypr2mat(PhotoScan.Vector([180,-20,180]))
#
# # for c in chunk.cameras:
# #     print(c.transform)
#
#
#
# # ## Find first aligned image
# # first = next(c for c in chunk.cameras if c.transform)
# # print(first.photo.path)
# # first.reference.rotation = PhotoScan.Vector([45,45,45])
#
# project_path="%s/%s" % (os.getcwd(), args.projectname)
# print(project_path)
# doc.save(path=project_path, chunks=doc.chunks)
#
# ## Try exporting a panorama
