#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides a GUI for the Enigma emulator in emulator.py. Uses Kivy.
"""

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, ObjectProperty, NumericProperty, \
  StringProperty
from kivy.graphics import Color, Triangle, Rectangle, Line
from kivy.clock import Clock

from string import ascii_uppercase as alphabet, ascii_lowercase as alpha_lower
import ast

import emulator as em

class Rotor(Widget):
  
  cipher = DictProperty({
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
    'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U',
    'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
  })
  
  rotor_num = NumericProperty(-1)
  rotor_pos = NumericProperty(0)
  
  char_in = StringProperty('')
  char_out = StringProperty('')
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  def on_rotor_num(self, instance, rotor_num):
    self.cipher.update({alpha: char for alpha, char in
                        zip(alphabet, enigma.rotors[rotor_num].cipher)})
    
    rotor_cbs, rotor_back_cbs = [None, None, None], [None, None, None]
    rotor_cbs[rotor_num] = self.callback_in
    rotor_back_cbs[rotor_num] = self.callback_out
    
    enigma.set_callbacks(rotors=tuple(rotor_cbs),
                         rotors_back=tuple(rotor_back_cbs))
  
  def callback_in(self, char_in, char_out, cipher, pos):
    self.char_in = char_in
    self.rotor_pos = pos
  
  def callback_out(self, char_in, char_out, cipher, pos):
    self.char_out = char_out
    self.rotor_pos = pos

class Plugboard(Widget):
  
  swaps = DictProperty({
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G',
    'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
    'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U',
    'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
  })
  
  char_in = StringProperty('')
  char_out = StringProperty('')
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    enigma.set_callbacks(
      plugboard=self.callback_in, plugboard_back=self.callback_out)
  
  def callback_in(self, char_in, char_out, swaps):
    self.swaps.update(swaps)
    self.char_in = char_in
  
  def callback_out(self, char_in, char_out, swaps):
    self.swaps.update(swaps)
    self.char_out = char_out
  
  def update_swaps(self, swaps_str):
    try:
      if not swaps_str.endswith(','):
        swaps_str += ','
      
      if swaps_str == ',':
        swaps_str = '()'
      
      swaps_pairs = ast.literal_eval(swaps_str)
      
      # Make sure it's a tuple
      if not isinstance(swaps_pairs, tuple):
        raise ValueError('not a tuple')
      
      # Make sure each pair is a 2-tuple of 1-length strings
      if len(swaps_pairs) > 0 and not all(
                isinstance(pair, tuple) and len(pair) == 2
                and isinstance(pair[0], str) and isinstance(pair[1], str)
                and len(pair[0]) == len(pair[1]) == 1
              for pair in swaps_pairs):
        print(swaps_pairs)
        raise ValueError('not tuple of 2-tuples of 1-length strings')
      
      # Make sure there's no duplicate chars
      chars_used = []
      for pair in swaps_pairs:
        for char in pair:
          if char in chars_used:
            raise ValueError('duplicates')
          chars_used.append(char)
    
    except ValueError as e:
      # Highlight the box in red
      self.parent.parent.ids.swaps_input.background_color = [1, 0.5, 0.5, 1]
      print('caught:')
      print(e)
    
    else:
      # Clear any highlighting
      self.parent.parent.ids.swaps_input.background_color = [1, 1, 1, 1]
      
      # Update swaps
      enigma.plugboard.reset()
      for char0, char1 in swaps_pairs:
        enigma.plugboard.swap(char0, char1)
      
      self.swaps = {char: char for char in alphabet}
      self.swaps.update(enigma.plugboard.swaps)
    
    finally:
      # Reopen the actual Enigma input
      gui = self.parent.parent
      gui._keyboard = Window.request_keyboard(gui._keyboard_closed, gui)
      gui._keyboard.bind(on_key_down=gui._on_keyboard_down)

class EmulatorGui(BoxLayout):
  
  gui = ObjectProperty(None)
  
  rotor0 = ObjectProperty(None)
  rotor1 = ObjectProperty(None)
  rotor2 = ObjectProperty(None)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down=self._on_keyboard_down)
  
  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard = None
  
  def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] in alphabet:
      char = keycode[1]
    elif keycode[1] in alpha_lower:
      char = keycode[1].upper()
    else:
      # Ignore non-alphabetic characters
      return
    
    self.ids.plaintext.text += char
    
    encrypted = enigma.encrypt(char)
    self.ids.ciphertext.text += encrypted
  
  def on_build(self):
    self.rotor0.rotor_num = 0
    self.rotor1.rotor_num = 1
    self.rotor2.rotor_num = 2
  
  def reset(self):
    enigma.reset()
    self.ids.plaintext.text = 'plaintext: '
    self.ids.ciphertext.text = 'ciphertext: '
    
    for rotor in [self.rotor0, self.rotor1, self.rotor2]:
      rotor.rotor_pos = 0
      rotor.char_in = ''
      rotor.char_out = ''
    
    self.plugboard.char_in = ''
    self.plugboard.char_out = ''

class EmulatorApp(App):
  
  def build(self):
    gui = EmulatorGui()
    gui.on_build()
    return gui

if __name__ == '__main__':
  enigma = em.Enigma(
    (em.ROTOR_III, em.ROTOR_II, em.ROTOR_I), (0, 0, 0), em.REFLECTOR_B, [])
  EmulatorApp().run()