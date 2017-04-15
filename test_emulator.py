#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import emulator as emul
import string

def test_get_letter_pos():
  for pos, (upper, lower) in enumerate(zip(string.ascii_lowercase,
      string.ascii_uppercase)):
    assert emul.get_letter_pos(upper) == emul.get_letter_pos(lower) == pos

def test_get_letter_pos_reject():
  with pytest.raises(ValueError):
    emul.get_letter_pos('&')

class TestRotor:
  
  def test_init_rejects_long_cipher(self):
    with pytest.raises(ValueError):
      emul.Rotor(string.ascii_uppercase * 2, [])
  
  def test_init_rejects_short_cipher(self):
    with pytest.raises(ValueError):
      emul.Rotor('ABC', [])
  
  def test_init_rejects_nonalphabetical_cipher(self):
    with pytest.raises(ValueError):
      emul.Rotor('1234567890!@#$%^&*()_-+=[]', [])
  
  def test_init_rejects_mixed_cipher(self):
    with pytest.raises(ValueError):
      emul.Rotor('@BCD3FG#!JKLMNOPQR$TUVWXYZ', [])
  
  def test_init_normalizes_cipher_case(self):
    rotor = emul.Rotor('ABcdEfGhIjklMnoPQRstuVWxyZ', [])
    assert rotor.cipher == list(string.ascii_uppercase)
  
  def test_init_allows_empty_turnover(self):
    rotor = emul.Rotor(string.ascii_uppercase, [])
    assert rotor.turnovers == []
  
  def test_init_rejects_improper_turnover_list(self):
    with pytest.raises(ValueError):
      emul.Rotor(string.ascii_uppercase, ['AB', 'CD'])
  
  def test_init_sets_turnovers_correctly_str_len1(self):
    rotor = emul.Rotor(string.ascii_uppercase, 'A')
    assert rotor.turnovers == [0]
  
  def test_init_sets_turnovers_correctly_str_len3(self):
    rotor = emul.Rotor(string.ascii_uppercase, 'ABC')
    assert rotor.turnovers == [0, 1, 2]
  
  def test_init_sets_turnovers_correctly_list(self):
    rotor = emul.Rotor(string.ascii_uppercase, ['A', 'B', 'C'])
    assert rotor.turnovers == [0, 1, 2]
  
  def test_init_normalizes_turnover_case(self):
    rotor = emul.Rotor(string.ascii_uppercase, 'aBCdeF')
    assert rotor.turnovers == [0, 1, 2, 3, 4, 5]
  
  def test_init_defaults_thin_false(self):
    rotor = emul.Rotor(string.ascii_uppercase, [])
    assert not rotor.thin
  
  def test_init_can_set_thin_true(self):
    rotor = emul.Rotor(string.ascii_uppercase, [], thin=True)
    assert rotor.thin
  
  def test_reset(self):
    rotor = emul.Rotor(string.ascii_uppercase, [])
    rotor.ring_pos = 7
    rotor.position = 3
    rotor.just_turned_over = True
    
    rotor.reset()
    assert rotor.ring_pos == rotor.position == 0
    assert not rotor.just_turned_over
  
  def test_reset_position(self):
    rotor = emul.Rotor(string.ascii_uppercase, [])
    rotor.ring_pos = 7
    rotor.position = 3
    rotor.just_turned_over = True
    
    rotor.reset_position()
    assert rotor.ring_pos == 7
    assert rotor.position == 0
    assert not rotor.just_turned_over