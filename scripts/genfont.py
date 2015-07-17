#!/usr/bin/env python2

# An ugly script to generate fonts from multi-layers SFD file.
# Copyright (c) 2014, Sungsit Sawaiwan
#
# argv[1] = sfd file
# argv[2] = font family name
# NOT implemented yet: argv[3] = desired font extentsion (otf, ttf, woff, svg)
#
# Usage: python genOTF.py <sdf file> <font family name> <font extention>

import sys,os
from datetime import datetime
import fontforge

fontfile = sys.argv[1]
font = fontforge.open(fontfile)

print sys.argv[2],'generated date:', datetime.now()
sep = '\n========================================================\n'

print sep
print 'SFD source file: ', fontfile

# Change copyright text here
font.copyright = 'Copyright (c) 2014, Sungsit Sawaiwan (http://sungsit.com | gibbozer [at] gmail [dot] com), with Reserved Font Names "BoonTook".'
font.version = '1.0.0'

# Check some font properties

print sep

fontdir = './fonts-unhinted/' + sys.argv[3] + '/'
feadir = './features/'
dirs = [fontdir, feadir]
for d in dirs:
  if not os.path.exists(d):
    os.makedirs(d)

# save full feature file
font.generateFeatureFile(feadir + sys.argv[2] + '.fea')


cnt = font.layer_cnt

i = 0
while (i < cnt):
  if i > 1: # Exclude first two layers (Back & Fore)
    layername = font.layers[i].name

    #font.layers[layername].select
    fullname = sys.argv[2] + ' ' + layername

    psname = fullname.replace(' ','-')
    font.fontname = psname
    font.fullname = fullname
    filename = psname

    if layername.endswith(' Oblique'):
      subfamily = layername.strip(' Oblique')
      font.italicangle = -9.0
      # import italic .fea
    else:
      subfamily = layername
      font.italicangle = 0.0

    font.familyname = sys.argv[2] + ' ' + subfamily

    newname = filename + '.' + sys.argv[3]

    # gen layer to font file
    font.generate(fontdir + newname, flags = ('round','opentype'), layer = layername)

    # checking
    nfile = fontdir + newname
    n = fontforge.open(nfile)

    # print some font prop 
    print 'Font family:', n.familyname
    print 'PS name:', n.fontname
    print 'Human name:', n.fullname
    print 'Font weight:', n.weight
    print 'OS2 weight:', n.os2_weight
    print 'Italic angle:', n.italicangle
    print 'File path:', nfile
    print 'Font version:', n.version

    n.unlinkReferences()
    n.correctDirection()
    n.removeOverlap()
    n.generate(nfile)
    n.close()

    print sep
  i += 1

print font.copyright

font.save()
font.close()
