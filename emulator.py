#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the logic to emulate one of several enigma machines used by
the Nazis during World War 2.
"""

class Plugboard:
  """
  Emulates the plugboard of the Enigma machine, which allowed the operator to
  swap certain letters on the keyboard. For example, if F and Q were swapped, F
  would be changed to Q before going into the rotors.
  
  To swap two letters, call `swap()` with the two letters you wish to swap.
  Alternatively, call `swap_all()` to swap a list of characters as varargs.
  To get the encoding of a letter through the plugboard, call `encode()` with
  your letter and the encoding will be returned. To reset the plugboard, call
  `reset()`.
  """
  
  def __init__(self):
    self.reset()
  
  def reset(self):
    # self.swaps is a bidict; that is, each entry is added twice.
    # One is {key: value} and the other is {value: key}
    # This way we can look up in reverse
    self.swaps = {}
  
  def swap(self, char1, char2):
    # Add char1 and char2 both to the dict
    char1, char2 = char1.upper(), char2.upper()
    if char1 not in self.swaps and char2 not in self.swaps:
      self.swaps[char1] = char2
      self.swaps[char2] = char1
  
  def swap_all(self, *chars):
    if len(chars) % 2 != 0:
      raise ValueError('Must be an even number of arguments to swap_all()')
    
    for swap in zip(chars[::2], chars[1::2]):
      self.swap(swap)
  
  def encode(self, char):
    try:
      return self.swaps[char]
    except KeyError:
      return char