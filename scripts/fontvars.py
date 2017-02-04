#!/usr/bin/env fontforge
#
# Copyright (c) 2017, Sungsit Sawaiwan (https://sungsit.com | gibbozer [at] gmail [dot] com).
#
# This Font Software is licensed under the SIL Open Font License, Version 1.1 (OFL).
# You should have received a copy of the OFL License along with this file.
# If not, see http://scripts.sil.org/OFL
#

# This script will create SFD files from multi-layers source to prepare for later build process
# and it will only work with FontForge's Python extension.
import fontforge
import os
import subprocess
import shutil
import time
import datetime

# Font props
family = 'BoonTook'
version = '3.0'
foundry = 'FontUni'
os2_vendor = 'FUni'
foundry_url = 'https://fontuni.com/'
designer = 'Sungsit Sawaiwan'
designer_url = 'https://sungsit.com/'
license_url = 'http://scripts.sil.org/OFL'
copyright = 'Copyright 2014-2017, Sungsit Sawaiwan (https://fontuni.com | uni@fontuni.com). This Font Software is licensed under the SIL Open Font License, Version 1.1 (http://scripts.sil.org/OFL).'

# Building sources
feature_dir = 'sources/'
sources = ['sources/boontook-roman.sfd','sources/boontook-oblique.sfd']
features = ['boontook-roman', 'boontook-oblique']
layers = ['BoonTook', 'BoonTook Mon']

# Dir names
build_dir = 'fonts/'
if os.path.exists(build_dir):
  shutil.rmtree(build_dir)

sfd_dir = 'sfd/'
if os.path.exists(sfd_dir):
  shutil.rmtree(sfd_dir)

# Release packages
pkgs = ['otf', 'ttf', 'woff-otf', 'woff-ttf', 'woff2-otf', 'woff2-ttf']

# PS private values
def BlueValues(weight):
  switcher = {
    400: (-20, 0, 600, 620, 840, 860)
  }
  return switcher.get(weight)

def OtherBlues(weight):
  switcher = {
    400: (-260, -240)
  }
  return switcher.get(weight)

def StdHW(weight):
  switcher = {
    400: (180,)
  }
  return switcher.get(weight)

def StdVW(weight):
  switcher = {
    400: (280,)
  }
  return switcher.get(weight)

