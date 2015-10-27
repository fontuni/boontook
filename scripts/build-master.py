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
import shutil
import time
import datetime

# Predifined vars
foundry = 'FontUni'
family = 'BoonTook'
version = '2.0-beta2'
weights = [950]
sources = ['sources/boontook-roman.sfd','sources/boontook-oblique.sfd']
layers = ['Normal', 'Mon']
copyright =  'Copyright 2014-2015, Sungsit Sawaiwan (https://fontuni.com | uni@fontuni.com). This Font Software is licensed under the SIL Open Font License, Version 1.1 (http://scripts.sil.org/OFL).'
features = ['boontook-roman', 'boontook-oblique']
feature_dir = 'sources/'

build_dir = 'fonts/'
if os.path.exists(build_dir):
  shutil.rmtree(build_dir)

sfd_dir = 'sfd/'
if os.path.exists(sfd_dir):
  shutil.rmtree(sfd_dir)

unhinted_dir = build_dir + 'unhinted/'
if not os.path.exists(unhinted_dir):
  os.makedirs(unhinted_dir)

exts = ['otf', 'ttf', 'woff', 'woff2']

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
  font.fontname = font.familyname.replace(' ','-')
  font.fullname = font.fontname.replace('-',' ')
  font.appendSFNTName('English (US)', 'Manufacturer', foundry)
  font.appendSFNTName('English (US)', 'Preferred Family', family)
  font.os2_weight = 950
  style = 'Ultra'
  font.version = version
  font.copyright = copyright
  font.save()

  if source.endswith('-roman.sfd'):
    font.italicangle = 0.0
    font.mergeFeature(feature_dir + features[0] + '.fea')
    
  if source.endswith('-oblique.sfd'):
    font.italicangle = -9.0
    font.mergeFeature(feature_dir + features[1] + '.fea')
    
  # loop through each layer & save it as sfd files
  # then generate ttf, autohint & make woff + woff2
  for layer in layers:
    
    if layer.startswith('Mon'):
      font.familyname = family + ' Mon'
      font.fontname = font.familyname.replace(' ','-')
      font.fullname = font.fontname.replace('-',' ')
      style = 'Mon Ultra'
      font.appendSFNTName('English (US)', 'SubFamily', '')
      font.appendSFNTName('English (US)', 'SubFamily', 'Regular')
      font.appendSFNTName('English (US)', 'Preferred Styles', style)

      if source.endswith('-oblique.sfd'):
        font.appendSFNTName('English (US)', 'SubFamily', '')
        font.appendSFNTName('English (US)', 'SubFamily', 'Oblique')
        font.appendSFNTName('English (US)', 'Preferred Styles', style + ' Oblique')
        font.fontname += '-Oblique'
        font.fullname += ' Oblique'
        
    else:
      font.fontname = font.familyname.replace(' ','-')
      font.fullname = font.fontname.replace('-',' ')
      font.appendSFNTName('English (US)', 'SubFamily', '')
      font.appendSFNTName('English (US)', 'SubFamily', 'Regular')
      font.appendSFNTName('English (US)', 'Preferred Styles', style)
      
      if source.endswith('-oblique.sfd'):
        font.appendSFNTName('English (US)', 'SubFamily', '')
        font.appendSFNTName('English (US)', 'SubFamily', 'Oblique')
        font.appendSFNTName('English (US)', 'Preferred Styles', style + ' Oblique')
        font.fontname += '-Oblique'
        font.fullname += ' Oblique'
  
    # UniqueID with timestamp
    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    uniqueid = foundry + ' : ' + font.fullname + ' ' + version + ' : ' + ts
    font.appendSFNTName('English (US)', 'UniqueID', uniqueid)

    otf = fontPath('otf',font.fontname)
    ttf = fontPath('ttf',font.fontname)
    woff = fontPath('woff',font.fontname)
    woff2 = fontPath('woff2',font.fontname)
    tempwoff2 = build_dir + 'ttf/' + font.fontname + '.woff2'

    # generate otf
    otfgenflags  = ('opentype', 'PfEd-lookups')
    font.generate(otf, flags=otfgenflags, layer = layer)
    print(font.fullname, 'OTF instance generated.')

    # save sfd
    otf2Sfd(otf,sfd_dir)

    # generate unhinted ttf
    ttfgenflags  = ('opentype', 'no-hints')
    ttfunhinted = unhinted_dir + font.fontname + '-unhinted.ttf'
    font.generate(ttfunhinted, flags=ttfgenflags, layer = layer)
    print(font.fullname, 'Unhinted TTF instance generated.')

    # ttfautohint
    ttfHint(ttfunhinted,ttf)
    fontOptimize(ttf)
    printFontInfo(ttf)
    print(font.fullname, 'TTF autohinted.')

    # hinted ttf to woff
    ttf2Woff(ttf,woff,ttfgenflags)
    print(font.fullname, 'WOFF instance generated.')

    # hinted ttf to woff2
    subprocess.call(['woff2_compress',ttf])
    os.rename(tempwoff2, woff2)
    print(font.fullname, 'WOFF2 instance generated.')

  font.close()

for source in sources:
  buildFont(source,family)

# Create zip package for each font extension
def fontZip(family,version,ext):
  path = build_dir + ext + '/'
  package = family + '-v' + version + '-' + ext + '.zip'
  shutil.copy2('OFL.txt', path)
  os.chdir(build_dir)
  subprocess.call(['zip', '-r', package, ext])
  os.remove(ext + '/OFL.txt')
  os.chdir('..')
  print(package, 'created.')

for ext in exts:
  fontZip(family,version,ext)
