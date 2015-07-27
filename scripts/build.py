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
version = '2.0-alpha2'
source = 'sources/boontook-master.sfd'
weights = [950]
layers = ['Normal', 'Normal Oblique', 'Mon', 'Mon Oblique']
copyright =  'Copyright 2014-2015, Sungsit Sawaiwan (https://fontuni.com | uni@fontuni.com). This Font Software is licensed under the SIL Open Font License, Version 1.1 (http://scripts.sil.org/OFL).'
features = ['boontook-master']
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
    '--strong-stem-width=gGD',
    '--hinting-range-min=8',
    '--hinting-range-max=50',
    '--hinting-limit=200',
    '--increase-x-height=12',
    '--no-info',
    '--verbose',
    unhinted,
    hinted
  ])

def ttf2Woff(ttf,woff,genflags):
  font = fontforge.open(ttf)
  font.generate(woff, flags=genflags)
  font.close()

def buildFont(source,family):
  font = fontforge.open(source)
  font.familyname = family
  font.weight = str(weight)
  font.os2_weight = weight
  font.version = version
  font.copyright = copyright
  font.save()

  for feature in features:
    font.mergeFeature(feature_dir + feature + '.fea')

  for layer in layers:
    layername = font.layers[layer].name
    subfamily = ''
    font.italicangle = 0

    if layername.startswith('Mon'):
      subfamily += '-Mon'
      
    if layername.endswith('Oblique'):
      subfamily += '-Oblique'
      font.italicangle = -9.0
      
    font.fontname = family + subfamily
    font.fullname = font.fontname.replace('-',' ')

    genflags  = ('opentype', 'PfEd-lookups', 'no-hints')
    ttfunhinted = unhinted_dir + font.fontname + '-unhinted.ttf'
    font.generate(ttfunhinted, flags=genflags, layer = layername)

    ttf = build_dir + font.fontname + '.ttf'
    woff = build_dir + font.fontname + '.woff'

    ttfHint(ttfunhinted,ttf)
    printFontInfo(ttf)

    ttf2Woff(ttf,woff,genflags)
    subprocess.call(['woff2_compress',ttf])

  font.save('sources/boontook-master-temp.sfd')
  font.close()

if not os.path.exists(unhinted_dir):
  os.makedirs(unhinted_dir)

for weight in weights:
  buildFont(source,family)
