#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
  base = 'Win32GUI'

setup(name='Enigma Emulator',
      version='1.0'
      description="A visual for Mr. Gillespie's CHC2DG WWII visual project",
      executables=[Executable('guiapp.py', base=base)])