#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides a GUI for the Enigma emulator in emulator.py. Uses Kivy.
"""

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, ObjectProperty
from kivy.graphics import Color, Triangle, Rectangle, Line
from kivy.clock import Clock

import emulator as em

class Plugboard(Widget):
  
  swaps = DictProperty({
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
    'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U',
    'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
  })
  
  def activate(self, char, in_=True): # in_ is whether the signal is in or out
    # Find bottom label to draw on
    label = self.ids['pb%s_btm' % char]
    
    # Draw an arrow below it
    with label.canvas:
      if in_:
        Color(0, 1, 0)
      else:
        Color(1, 0, 0)
      
      triangle_x = label.center_x
      triangle_y = label.center_y - 6
      
      Triangle(points=[triangle_x, triangle_y,
                       triangle_x - 4, triangle_y - 6,
                       triangle_x + 4, triangle_y - 6])
      
      rect_x = triangle_x - 2
      rect_y = triangle_y - 10
      
      Rectangle(pos=[rect_x, rect_y], size=[4, 6])
      
      # Redraw the line coloured
      other_label = self.ids['pb%s' % self.swaps[char]]
      Line(points=[label.center_x, label.center_y + 7,
                   other_label.center_x, other_label.center_y - 7])

class EmulatorGui(BoxLayout):
  
  plugboard = ObjectProperty(None)
  
  def activate_pb(self, dt):
    self.plugboard.activate('A')

class EmulatorApp(App):
  
  def build(self):
    gui = EmulatorGui()
    Clock.schedule_once(gui.activate_pb, 0.5)
    return gui

if __name__ == '__main__':
  EmulatorApp().run()