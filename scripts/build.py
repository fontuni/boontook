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
import glob

# Predifined vars
foundry = 'FontUni'
family = 'BoonTook'
version = '2.0.1'
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

def fontPath(ext,name):
  path = build_dir + ext
  if not os.path.exists(path):
    os.makedirs(path)
  fontfile = path + '/' + name + '.' + ext
  return fontfile

def printFontInfo(fontfile):
  font = fontforge.open(fontfile)
  print('\nFont File: ' + fontfile)
  print('Family Name: ' + font.familyname)
  print('Font Name: ' + font.fontname)
  print('Full Name: ' + font.fullname)
  print('Font Weight: ' + font.weight)
  print('OS2 Weight: ' + str(font.os2_weight))
  print('Oblique Angle: ' + str(font.italicangle))
  print('Font Version: ' + font.version)
  print('Font Copyright: ' + font.copyright)
  font.close()

def otf2Sfd(otf,sfd_dir):
  
  font = fontforge.open(otf)
  sfd = sfd_dir + font.fontname + '.sfd'
  if not os.path.exists(sfd_dir):
    os.makedirs(sfd_dir)

  font.appendSFNTName('English (US)', 'UniqueID', '')
  
  weight = font.os2_weight
  font.private['BlueValues'] = (-20, 0, 600, 620, 840, 860)
  font.private['OtherBlues'] = (-260, -240)
  font.private['BlueShift'] = 0,
  font.private['StdHW'] = 180,
  font.private['StdVW'] = 280,
  font.private['StemSnapH'] = (90, 120, 140, 150, 180, 200, 210, 240)
  font.private['StemSnapV'] = (270, 280)
  font.selection.all()
  font.autoHint()
  font.save(sfd)
  font.private.guess('StemSnapH')
  font.private.guess('StemSnapV')
  font.private.guess('BlueShift')
  font.selection.all()
  font.autoHint()
  font.save(sfd)
  print(sfd, 'file saved.')
  font.close()

def buildSFD(source,family):

  # prepare master
  font = fontforge.open(source)
  font.familyname = family
  font.fontname = font.familyname.replace(' ','-')
  font.fullname = font.fontname.replace('-',' ')
  font.appendSFNTName('English (US)', 'Manufacturer', foundry)
  font.appendSFNTName('English (US)', 'Preferred Family', family)
  font.os2_weight = 400
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
      font.appendSFNTName('English (US)', 'Preferred Family', family + ' Mon')
      font.appendSFNTName('English (US)', 'SubFamily', '')
      font.appendSFNTName('English (US)', 'SubFamily', 'Regular')
      font.appendSFNTName('English (US)', 'Preferred Styles', style)
      font.appendSFNTName('English (US)', 'Compatible Full', family)

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
      font.appendSFNTName('English (US)', 'Compatible Full', family + ' Mon')
      
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

  font.close()

for source in sources:
  buildSFD(source,family)

# Generate & hint SFD files

exts = ['otf', 'ttf', 'woff', 'woff2', 'eot', 'svg']

def otfHint(unhinted,hinted):
  subprocess.call([
    'autohint',
    '-q',
    '-o',
    hinted,
    unhinted
  ])
  print(hinted, 'autohinted.')

def ttfHint(unhinted,hinted):
  subprocess.call([
    'ttfautohint',
    '--default-script=latn',
    '--fallback-script=thai',
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
  print(hinted, 'autohinted.')

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
  print(fontfile, 'optimized.')

# http://wizard.ae.krakow.pl/~jb/ttf2woff/
def ttf2Woff(ttf,woff):
  subprocess.call([ 'ttf2woff', '-v', ttf, woff ])
  print(woff, 'instance generated.')

def ttf2Woff2(ttf,woff2):
  subprocess.call(['woff2_compress',ttf])
  (root, ext) = os.path.splitext(ttf)
  os.rename(root + '.woff2', woff2)
  print(woff2, 'instance generated.')

def ttf2Eot(ttf,eot):
  os.system('ttf2eot <' + ttf + '>' + eot)
  print(eot, 'instance generated.')

def buildFont(sfd):
  font = fontforge.open(sfd)

  # UniqueID with timestamp
  ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
  uniqueid = foundry + ' : ' + font.fullname + ' ' + font.version + ' : ' + ts
  font.appendSFNTName('English (US)', 'UniqueID', uniqueid)

  otf = fontPath('otf',font.fontname)
  ttf = fontPath('ttf',font.fontname)
  woff = fontPath('woff',font.fontname)
  woff2 = fontPath('woff2',font.fontname)
  eot = fontPath('eot',font.fontname)
  svg = fontPath('svg',font.fontname)
  tempwoff2 = build_dir + 'ttf/' + font.fontname + '.woff2'

  # generate otf
  otfgenflags  = ('opentype', 'PfEd-lookups')
  otfunhinted = unhinted_dir + font.fontname + '-unhinted.otf'
  font.generate(otfunhinted, flags=otfgenflags)
  print(otfunhinted, 'instance generated.')

  # AFDKO autohint
  otfHint(otfunhinted,otf)
  fontOptimize(otf)
  printFontInfo(otf)

  # generate unhinted ttf
  ttfgenflags  = ('opentype', 'no-hints')
  ttfunhinted = unhinted_dir + font.fontname + '-unhinted.ttf'
  font.generate(ttfunhinted, flags=ttfgenflags)
  print(ttfunhinted, 'instance generated.')

  # ttfautohint
  ttfHint(ttfunhinted,ttf)
  fontOptimize(ttf)
  printFontInfo(ttf)

  # ttf2woff
  ttf2Woff(ttf,woff)

  # ttf2woff2
  ttf2Woff2(ttf,woff2)

  # ttf2eot
  ttf2Eot(ttf,eot)

  # gen svg
  font.generate(svg, flags=otfgenflags)
  print(svg, 'instance generated.')

  font.close()

for sfd in sorted(glob.glob('./sfd/*.sfd')):
  buildFont(sfd)

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

exts = ['otf', 'ttf', 'woff', 'woff2', 'eot', 'svg']

for ext in exts:
  fontZip(family,version,ext)
