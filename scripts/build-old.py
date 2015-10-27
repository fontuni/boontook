#!/usr/bin/env fontforge
#
# Copyright (c) 2015, Sungsit Sawaiwan (https://sungsit.com | gibbozer [at] gmail [dot] com).
#
# This Font Software is licensed under the SIL Open Font License, Version 1.1 (OFL).
# You should have received a copy of the OFL License along with this file.
# If not, see http://scripts.sil.org/OFL
#

# This script will only work with FontForge's Python extension.
import fontforge
import os
import subprocess

# Predifined vars
family = 'BoonTook'
version = '2.0-beta1'
source = 'sources/boontook-master.sfd'
weights = [950]
layers = ['Normal', 'Normal Oblique', 'Mon', 'Mon Oblique']
copyright =  'Copyright 2014-2015, Sungsit Sawaiwan (https://fontuni.com | uni@fontuni.com). This Font Software is licensed under the SIL Open Font License, Version 1.1 (http://scripts.sil.org/OFL).'
features = ['boontook-normal', 'boontook-oblique']
feature_dir = 'sources/'
build_dir = 'fonts/'
unhinted_dir = 'fonts/unhinted/'

def printFontInfo(fontfile):
  font = fontforge.open(fontfile)
  print('\nFont File: ' + fontfile)
  print('Family Name: ' + font.familyname)
  print('Font Name: ' + font.fontname)
  print('Full Name: ' + font.fullname)
  print('Font Weight: ' + font.weight)
  print('OS2 Weight: ' + str(font.os2_weight))
  print('Italic Angle: ' + str(font.italicangle))
  print('Font Version: ' + font.version)
  print('Font Copyright: ' + font.copyright)
  font.close()

def ttfHint(unhinted,hinted):
  subprocess.call([
    'ttfautohint',
    '--default-script=thai',
    '--fallback-script=latn',
    '--strong-stem-width=G',
    '--hinting-range-min=7',
    '--hinting-range-max=28',
    '--hinting-limit=50',
    '--increase-x-height=13',
    '--no-info',
    '--verbose',
    unhinted,
    hinted
  ])

# Optimize
def fontOptimize(fontfile):
  subprocess.call([
    'pyftsubset',
    fontfile,
    '--glyphs=*',
    '--layout-features=*',
    '--name-IDs=*',
    '--hinting',
    '--legacy-kern',
    '--notdef-outline',
    '--no-subset-tables+=DSIG',
    '--drop-tables-=DSIG',
    '--output-file=' + fontfile
  ])

def ttf2Woff(ttf,woff,genflags):
  font = fontforge.open(ttf)
  font.generate(woff, flags=genflags)
  font.close()

def fontPath(ext,name):
  path = build_dir + ext
  if not os.path.exists(path):
    os.makedirs(path)
  fontfile = path + '/' + name + '.' + ext
  return fontfile

def otf2Sfd(otf,sfd_dir):
  font = fontforge.open(otf)
  sfd = sfd_dir + font.fontname + '.sfd'
  if not os.path.exists(sfd_dir):
    os.makedirs(sfd_dir)
  font.appendSFNTName('English (US)', 'UniqueID', '')
  font.save(sfd)
  print(font.fontname, 'SFD files saved.')
  font.close()
  
def buildFont(source,family):

  # prepare master
  font = fontforge.open(source)
  font.familyname = family
  font.weight = str(weight)
  font.os2_weight = weight
  font.version = version
  font.copyright = copyright
  font.save()

  # loop through each layer & save it as sfd files
  # then generate ttf, autohint & make woff + woff2
  for layer in layers:

    layername = font.layers[layer].name
    subfamily = ''
    font.italicangle = 0.0

    if layername.startswith('Mon'):
      subfamily += '-Mon'
      
    if layername.endswith('Oblique'):
      subfamily += '-Oblique'
      font.italicangle = -9.0

    font.fontname = family + subfamily
    font.fullname = font.fontname.replace('-',' ')

    tempsfd = 'sources/'+ font.fontname +'-temp.sfd'
    font.save(tempsfd)

    temp = fontforge.open(tempsfd)

    if temp.fullname.endswith('Oblique'):
      temp.mergeFeature(feature_dir + features[1] + '.fea')
    else:
      temp.mergeFeature(feature_dir + features[0] + '.fea')

    genflags  = ('opentype', 'PfEd-lookups', 'no-hints')
    ttfunhinted = unhinted_dir + font.fontname + '-unhinted.ttf'

    # generate unhinted ttf
    temp.generate(ttfunhinted, flags=genflags, layer = layername)
    print(font.fullname, 'TTF instance generated.')

    temp.close()
    subprocess.call(['rm',tempsfd])

    ttf = build_dir + font.fontname + '.ttf'
    woff = build_dir + font.fontname + '.woff'

    # ttfautohint
    ttfHint(ttfunhinted,ttf)
    printFontInfo(ttf)
    print(font.fullname, 'TTF autohinted.')

    # hinted ttf to woff
    ttf2Woff(ttf,woff,genflags)
    print(font.fullname, 'WOFF instance generated.')

    # hinted ttf to woff2
    subprocess.call(['woff2_compress',ttf])
    print(font.fullname, 'WOFF2 instance generated.')

  font.save('sources/boontook-master-temp.sfd')
  font.close()

if not os.path.exists(unhinted_dir):
  os.makedirs(unhinted_dir)

for weight in weights:
  buildFont(source,family)