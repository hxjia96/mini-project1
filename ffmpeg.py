#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 19:47:46 2018

@author: ece-student
"""

import ffmpeg

def makevideo(path):
#    (
#        ffmpeg
#        .input(path, pattern_type='glob', framerate=25)
##        .filter('deflicker', mode='pm', size=10)
##        .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
#        .output('movie.mp4', preset='slower', pix_fmt='yuv420p')
#        .view(filename='filter_graph')
#        .run()
#)
    picinput = ffmpeg.input(path, framerate=24, r = 1)
    videooutput = ffmpeg.output(picinput, 'movie.mp4')
    ffmpeg.run(videooutput)
#    (
#        ffmpeg
#        .input(path, pattern_type='glob', framerate=25)
#        .output('movie.mp4', pix_fmt='yuv420p')
#        .run()
#    )

if __name__ == '__main__':
    path = 'image%03d.png'
    makevideo(path)