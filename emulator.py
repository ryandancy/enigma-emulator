#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the logic to emulate one of several enigma machines used by
the Nazis during World War 2.
"""

from string import ascii_letters, ascii_uppercase

def get_letter_pos(char):
  """
  Get a letter's position in the alphabet. For example:
      get_letter_pos('A') == 0
      get_letter_pos('B') == 1
      get_letter_pos('Z') == 25
  """
  
  if 'A' <= char <= 'Z':
    return ord(char) - ord('A')
  elif 'a' <= char <= 'z':
    return ord(char) - ord('a')
  else:
    raise ValueError('%s is not alphabetical' % char)

class Rotor:
  """
  Emulates a rotor in an Enigma machine. The rotors each perform a substitution
  cipher, which then rotates to change the cipher.
  
  To initialize the rotor, call `__init__()` with the cipher string and the list
  of turnover positions, which can also be a string. To encrypt a character with
  the rotor, call `encrypt()` with the character to encrypt and optionally
  whether to rotate the rotor. To "reverse-encrypt" a character, meaning run the
  character through the rotor the opposite way, call `reverse_encrypt()` with
  the character. To find out whether the next rotor in the chain should be
  rotated, call `should_turnover()`. To set the offset of the ring set
  `ring_pos`.
  """
  
  def __init__(self, cipher, turnovers, thin=False):
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
    :param thin: Whether the rotor is thin; i.e. it's a thin reflector or rotors
      Beta or Gamma.
    """
    
    if len(cipher) != 26:
      raise ValueError('Cipher must be 26 characters long (got %s)' % cipher)
    if set(cipher) > set(ascii_letters):
      raise ValueError('Cipher must be alphabetical (got %s)' % cipher)
    
    if any(len(turnover) > 1 for turnover in turnovers):
      raise ValueError('If using a list, each turnover must be 1 character long'
        ' (got %s)' % turnovers)
    
    self.thin = thin
    
    self.cipher = list(''.join(cipher).upper())
    
    # self.turnovers is a list of positions at which to turn over
    self.turnovers = list(get_letter_pos(turnover.upper())
                          for turnover in turnovers)
    
    self.reset()
  
  def reset(self):
    self.ring_pos = 0
    self.reset_position()
  
  def reset_position(self):
    self.position = 0
    self.just_turned_over = False
  
  def encrypt(self, char, turnover=False):
    cipher_pos = get_letter_pos(char) + self.position + self.ring_pos
    encrypted = self.cipher[cipher_pos % 26]
    
    self.just_turned_over = turnover
    
    return encrypted
  
  def reverse_encrypt(self, char):
    cipher_pos = self.cipher.index(char)
    alphabet_pos = cipher_pos - self.position - self.ring_pos
    return ascii_uppercase[alphabet_pos % 26]
  
  def should_turnover(self, rotors): # should the NEXT one turnover
    return (
      (self.just_turned_over and (self.position - 1) % 26 in self.turnovers) or
      # This is for double stepping; the 2nd rotor will turnover a second time
      # in a row if it's in its own turnover position.
      (rotors.index(self) == 0 and rotors[1].just_turned_over
        and rotors[1].position in rotors[1].turnovers))
  
  def turnover(self):
    self.position += 1
    self.position %= 26

ROTOR_I = Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
ROTOR_II = Rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
ROTOR_III = Rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')

ROTOR_IV = Rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
ROTOR_V = Rotor('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')

ROTOR_VI = Rotor('JPGVOUMFYQBENHZRDKASXLICTW', ['Z', 'M'])
ROTOR_VII = Rotor('NZJHGRCXMYSWBOUFAIVLPEKQDT', ['Z', 'M'])
ROTOR_VIII = Rotor('FKQHTLXOCBJSPDZRAMEWNIUYGV', ['Z', 'M'])

ROTOR_BETA = Rotor('LEYJVCNIXWPBQMDRTAKZGFUHOS', [], thin=True)
ROTOR_GAMMA = Rotor('FSOKANUERHMBTIYCWLQPZXVGJD', [], thin=True)

class Reflector(Rotor):
  
  def __init__(self, cipher, thin=False):
    super().__init__(cipher, [], thin=thin)
    
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
    return super().encrypt(char, turnover=False)

REFLECTOR_A = Reflector('EJMZALYXVBWFCRQUONTSPIKHGD')
REFLECTOR_B = Reflector('YRUHQSLDPXNGOKMIEBFZCWVJAT')
REFLECTOR_C = Reflector('FVPJIAOYEDRZXWGCTKUQSBNMHL')

REFLECTOR_B_THIN = Reflector('ENKQAUYWJICOPBLMDXZVFTHRGS', thin=True)
REFLECTOR_C_THIN = Reflector('RDOBJNTKVEHMLFCWZAXGYIPSUQ', thin=True)

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

class Enigma:
  """
  Emulates an Enigma machine used in WW2 by the Germans.
  """
  
  def __init__(self, *args):
    """
    Initialize this Enigma machine emulator. If any varargs are specified, they
    are passed to `configure()`.
    """
    
    self.plugboard = Plugboard()
    
    if args:
      self.configure(*args)
    else:
      self.configured = False
  
  def configure(self, rotors, rings, reflector, plugboard_swaps, rotor4=None):
    """
    Configure this Enigma machine emulator with the specified key.
    
    :param rotors: a 3-tuple of Rotors in the proper order.
    :param rings: a tuple of ring positions (ints), the same size as `rotors`.
    :param reflector: a Reflector for this Enigma.
    :param plugboard_swaps: a list of 2-tuple swaps for this Enigma's Plugboard.
    :param rotor4: a fourth Rotor that does not rotate.
    """
    
    if len(rotors) != 3:
      raise ValueError('`rotors` must be a 3-tuple in Enigma configuration '
                       '(use `rotor4` for a fourth, non-rotating rotor)')
    if any(rotor.thin for rotor in rotors):
      raise ValueError('Main rotors cannot be thin')
    
    # Fourth rotor *must* be used with a thin reflector for historical accuracy
    # Also fourth rotor must also be thin + thin rotors can't be used otherwise
    if rotor4 is None:
      if reflector.thin:
        raise ValueError('Thin reflector cannot be used if no fourth rotor')
    else:
      if not rotor4.thin:
        raise ValueError('Fourth rotor, if present, must be thin')
      if not reflector.thin:
        raise ValueError('If a fourth rotor is present, the reflector '
                         'must be thin')
      rotor4.reset()
      if len(rings) >= 4:
        rotor4.ring_pos = rings[3]
    
    self.rotors = rotors
    self.rotor4 = rotor4
    
    for rotor, ring_pos in zip(self.rotors, rings):
      rotor.reset()
      rotor.ring_pos = ring_pos
    
    self.reflector = reflector
    
    for char1, char2 in plugboard_swaps:
      self.plugboard.swap(char1, char2)
    
    self.configured = True
  
  def reset(self):
    """Reset all rotors to their default position to reuse the same key."""
    for rotor in self.rotors:
      rotor.reset_position()
  
  def encrypt(self, char):
    char = self.plugboard.encrypt(char)
    
    # Pass through rotors, queuing to turnover as necessary
    turnover = True # turn over first rotor
    rotors_to_turnover = []
    
    for rotor in self.rotors:
      if turnover:
        rotors_to_turnover.append(rotor)
      
      char = rotor.encrypt(char, turnover)
      turnover = rotor.should_turnover(self.rotors)
    
    # Pass through fourth rotor, if present, which does not turnover
    if self.rotor4 is not None:
      char = rotor.encrypt(char)
    
    # Pass through reflector
    char = self.reflector.encrypt(char)
    
    # Pass through fourth rotor in reverse, if present
    if self.rotor4 is not None:
      char = rotor.reverse_encrypt(char)
    
    # Pass through rotors backwards
    for rotor in reversed(self.rotors):
      char = rotor.reverse_encrypt(char)
    
    # Do all the turnovers after encryption
    for rotor in rotors_to_turnover:
      rotor.turnover()
    
    return char