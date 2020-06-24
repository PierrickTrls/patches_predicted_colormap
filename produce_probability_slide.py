# coding: utf8
import os
import csv
import numpy
import argparse
from tqdm import tqdm
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.cm
from skimage.io import imsave
from skimage.util import img_as_ubyte
from sklearn.cluster import KMeans
from openslide import OpenSlide
import json

parser = argparse.ArgumentParser()
parser.add_argument("--slidefolder", type=str, help="path to the original slide folder.")
parser.add_argument("--outputfolder", type=str,default=os.getcwd(), help="path to an output directory.")
parser.add_argument("--jsonfolder", type=str, help="path to the json containing patches positions")
parser.add_argument("--delta", type=int, default=598, help="closest distance between two patches.")
args = parser.parse_args()

outputfolder = args.outputfolder


def export_segimages(slide, data,outputfolder,filename):
    cmap = matplotlib.cm.viridis
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    # compute segmentation image
    xs = list()
    ys = list()
    for patch in data.keys():
        xs.append(data[patch]['x'])
        ys.append(data[patch]['y'])
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
    print(xmin,xmax,ymin,ymax)
    dx = xmax - xmin
    dy = ymax - ymin

    segimage = numpy.zeros((int(dy / args.delta) + 1, int(dx / args.delta) + 1, 3), float)
    print("created image's shape ",segimage.shape)

    for patch in data.keys():
        x = data[patch]['x'] - xmin
        y = data[patch]['y'] - ymin
        x = int(x / args.delta)
        y = int(y / args.delta)
        
        #Implemented for a binary classification problem
        if data[patch]['feature'][0] > 0.5:
            segimage[y, x, 0] = 1.0
            segimage[y, x, 1] = 1.0
            segimage[y, x, 2] = 1.0
        else: 
            segimage[y, x, 0] = 1.0
            segimage[y, x, 1] = 0.0
            segimage[y, x, 2] = 0.0

    imsave(os.path.join(outputfolder, filename+"_hypothese.png"), img_as_ubyte(segimage))
    print("working on ",slide)

    # slide = OpenSlide(slide)
    # img = slide.read_region((0, 0),6, slide.level_dimensions[6])
    # img = numpy.array(img)[:, :, 0:-1]
    # print(img.shape)
    # imsave(os.path.join(outputfolder, filename+"_original.png"), img)

for file in os.listdir(args.jsonfolder):
    filename = file[:-5]
    if filename in os.listdir(args.slidefolder):
        
        with open(file) as json_file: 
            data = json.load(json_file) 

        export_segimages(os.path.join(args.slidefolder, filename+".mrxs"),data, outputfolder,filename)

        