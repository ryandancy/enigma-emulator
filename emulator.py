#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the logic to emulate one of several enigma machines used by
the Nazis during World War 2.
"""

from string import ascii_letters

def get_letter_pos(char):
  """
  Get a letter's position in the alphabet. For example:
      get_letter_pos('A') == 0
      get_letter_pos('B') == 1
      get_letter_pos('Z') == 25
  """
  return ord(char.upper()) - ord('A')

class Rotor:
  """
  Emulates a rotor in an Enigma machine. The rotors each perform a substitution
  cipher, which then rotates to change the cipher.
  
  To initialize the rotor, call `__init__()` with the cipher string and the list
  of turnover positions, which can also be a string. To encrypt a character with
  the rotor, call `encrypt()` with the character to encrypt and optionally
  whether to rotate the rotor. To find out whether the next rotor in the chain
  should be rotated, call `should_turnover()`. To set the offset of the ring,
  set `ring_pos`.
  """
  
  def __init__(self, cipher, turnovers):
    """
    Initialize this rotor.
    
    :param cipher: A 26-char long string representing the substitution cipher
      this rotor performs, in alphabetical order. For example, the German
      Railway enigma rotor I's cipher was "JGDQOXUSCAMIFRVTPNEWKBLZYH", which
      means that A mapped to J, B to G, C to D, and so on.
    :param turnovers: A character or list of characters that represent the
      positions on the wheel (in plaintext) on which the rotor will rotate one
      position forward. For example, if the turnover is "D", then the rotor will
      rotate when going from D to E. A string longer than 1 character will be
      interpreted as a list of characters.
    """
    
    if len(cipher) != 26:
      raise ValueError('Cipher must be 26 characters long (got %s)' % cipher)
    if set(cipher) > ascii_letters:
      raise ValueError('Cipher must be alphabetical (got %s)' % cipher)
    
    if any(len(turnover) > 1 for turnover in turnovers):
      raise ValueError('If using a list, each turnover must be 1 character long'
        ' (got %s)' % turnovers)
    
    self.cipher = list(''.join(cipher).upper())
    
    # self.turnovers is a list of positions at which to turn over
    self.turnovers = list(get_letter_pos(turnover) for turnover in turnovers)
    
    self.ring_pos = 0
    self.position = 0
    
    self.just_turned_over = False
  
  def encrypt(self, char, turnover=False):
    cipher_pos = get_letter_pos(char) + self.position + self.ring_pos
    encrypted = self.cipher[cipher_pos % 26]
    
    if turnover:
      self.position += 1
      self.position %= 26
    
    self.just_turned_over = turnover
    
    return encrypted
  
  def should_turnover(self):
    return self.just_turned_over and self.position in self.turnovers

class Reflector(Rotor):
  
  def __init__(self, cipher):
    super().__init__(cipher, [])
    
    # Make sure the cipher's a proper reflector cipher
    # For this, each letter's number's position in the cipher must be the letter
    # with the position corresponding to the position of the original letter.
    # For example, if B was in position 0, A would have to be in position 1.
    # An example reflector cipher: EJMZALYXVBWFCRQUONTSPIKHGD
    
    for letter_pos, letter in enumerate(cipher):
      pos = get_letter_pos(letter)
      
      if get_letter_pos(cipher[pos]) != letter_pos:
        raise ValueError('Improper reflector cipher (got %s)' % cipher)
  
  def encrypt(self, char, turnover=False):
    # Ignore turnover, don't allow the reflector to turn over
    super().encrypt(char, turnover=False)

class Plugboard:
  """
  Emulates the plugboard of the Enigma machine, which allowed the operator to
  swap certain letters on the keyboard. For example, if F and Q were swapped, F
  would be changed to Q before going into the rotors.
  
  To swap two letters, call `swap()` with the two letters you wish to swap.
  Alternatively, call `swap_all()` to swap a list of characters as varargs.
  To get the encryption of a letter through the plugboard, call `encrypt()` with
  your letter and the encryption will be returned. To reset the plugboard, call
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
    if len(char1) > 1 or len(char2) > 1:
      raise ValueError('char1 and char2 must be 1-char strings (got %s and %s)'
        % (char1, char2))
    
    if char1 not in ascii_letters or char2 not in ascii_letters:
      raise ValueError('char1 and char2 must be alphabetical (got %s and %s)'
        % (char1, char2))
    
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
  
  def encrypt(self, char):
    try:
      return self.swaps[char]
    except KeyError:
      return char