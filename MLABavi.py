#!/usr/bin/python
#coding: utf-8

from gimpfu import *
import os
from subprocess import call
import numpy as np
from scipy.misc import imread

class MLABavi(object):
    
    def __init__(self, raw,  post):
        self.raw = raw
        self.post = post

    def import_avi(self):
        try:
            os.stat(os.path.dirname(__file__) +"/MLABavi")
            print "existuje .."
        except:
            os.mkdir(os.path.dirname(__file__) +"/MLABavi")
            print "je vytvoren novy"
        print "----------"
        print "ffmpeg -y -t 0 -i self.raw "+ self.raw + " " + os.path.dirname(__file__) +"/MLABavi" +"/image.png"
        print call(["ffmpeg -y -t 0 -i "+ self.raw + " " + os.path.dirname(__file__) +"/MLABavi" +"/image.png"], shell=True)
        print "pokračuji ------------------"
        window = gimp.Image(500, 500, GRAY)
        mImage = pdb.file_png_load(os.path.dirname(__file__) +"/MLABavi" +"/image.png", os.path.dirname(__file__) +"/MLABavi" +"/image.png")
        print mImage
        print window

        print "pokračuji ------------------"
      
        sarr= imread(os.path.dirname(__file__) +"/MLABavi" +"/image.png", True)
         
        mLayer = gimp.Layer(mImage, "SecondLayer", mImage.width, mImage.height, RGB_IMAGE, 100, NORMAL_MODE)
        mImage.add_layer(mLayer, 0)
      
        for l in mImage.layers:
            if not l.has_alpha:
                pdb.gimp_layer_add_alpha(l)

        arrOUT = np.zeros((mImage.height,mImage.width,4))

        print "x=",sarr.shape[0]
        print "y=",sarr.shape[1]

        for x in xrange(0,(sarr.shape[0]-1)/2):
            print x, " z ", sarr.shape[0]
            for y in xrange(0,(sarr.shape[1]-1)/2):
#
#                colourBGGR = [  (sarr[x*2+1][y*2+1]),  # BGGR
#                                (sarr[x*2+0][y*2+1] + sarr[x*2+1][y*2+0])/2,
#                                (sarr[x*2+0][y*2+0]),
#                                255]
#
#                colourRGGB = [  (sarr[x*2+0][y*2+0]),  # BGGR
#                                (sarr[x*2+0][y*2+1] + sarr[x*2+1][y*2+0])/2,
#                                (sarr[x*2+1][y*2+1]),
#                                255]
#
#                colourGBRG = [  (sarr[x*2+1][y*2+0]),  # BGGR
#                                (sarr[x*2+0][y*2+0] + sarr[x*2+1][y*2+1])/2,
#                                (sarr[x*2+0][y*2+1]),
#                                255]
#


                colourGRBG = [     (sarr[x*2+0][y*2+1]),  # BGGR
                                int((sarr[x*2+0][y*2+0] + sarr[x*2+1][y*2+1])/2),
                                    (sarr[x*2+1][y*2+0]),
                                    255]
#
#                colourORIG = [  (sarr[x][y]),  # BGGR
#                                (sarr[x][y]),
#                                (sarr[x][y]),
#                                255]
#
                colour = colourGRBG
                arrOUT[x*2+0][y*2+0] = (colour)     #Green
                arrOUT[x*2+1][y*2+1] = (colour)     #Green
                arrOUT[x*2+0][y*2+1] = (colour)     # UR - RED
                arrOUT[x*2+1][y*2+0] = (colour)     # DL - RED


        #for x in range(0,(sarr.shape[0])):  # radek
        #    print x, " z ", sarr.shape[0]
        #    for y in range(0,(sarr.shape[1])):  # sloupec
        #        if   (x%2==0 and y%2==0) or (x%2!=0 and y%2!=0):
        #            arrOUT[int(x)][int(y)] = [0,sarr[x][y],0,255]
        #        elif x%2==0 and y%2!=0:
        #            arrOUT[int(x)][int(y)] = [0,0,sarr[x][y],255]
        #        elif x%2!=0 and y%2==0:
        #            arrOUT[int(x)][int(y)] = [sarr[x][y],0,0,255]

        
        if self.post: # post-processing, který vyzaduje numpy pole
            try:
                pass
            except Exception, e:
                print e

        byte_image = np.array((arrOUT).round(0),np.uint8)
        self.pr = mImage.layers[0].get_pixel_rgn(0, 0, mImage.width, mImage.height)
        print byte_image.size, mImage.width * mImage.height * 4
        self.pr[0:mImage.width, 0:mImage.height] = byte_image.tostring()

        if self.post: # post-processing, který vyzaduje gimp vrstvu
            try:
                pdb.plug_in_c_astretch(mImage, mImage.layers[0])
                mImage.layers[0].update(0, 0, mImage.width, mImage.height)
            except Exception, e:
                print e

            
        gimp.Display(mImage)
        gimp.displays_flush()




def run(raw, post):
    mclass = MLABavi(raw, post)
    mclass.import_avi()

register(
    "MLAB_RAW_avi_processor",
    "Otevřít RAW .AVI video",
    "upravit RAW obrázek ...",
    "Roman Dvořák",
    "Roman Dvořák",
    "2015",
    "Otevřít MLAB avi",
    "",
    [       
            (PF_FILE, "raw", "Input AVI", None),
            #(PF_INT, "frame", "Video frame", 1),
            #(PF_INT, "max_height", "Maximum Height", 500),
            (PF_BOOL, "post", "Auto post-processing", True),
    ],
    [],
    run, menu="<Image>/File/Create"
)

main()
