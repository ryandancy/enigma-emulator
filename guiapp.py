#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides a GUI for the Enigma emulator in emulator.py. Uses Kivy.
"""

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import emulator as em

class EmulatorGui(BoxLayout):
  pass

class EmulatorApp(App):
  def build(self):
    return EmulatorGui()

if __name__ == '__main__':
  EmulatorApp().run()