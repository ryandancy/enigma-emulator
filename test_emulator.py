#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import emulator as emul
import string

def test_get_letter_pos():
  for pos, (upper, lower) in enumerate(zip(string.ascii_lowercase,
      string.ascii_uppercase)):
    assert emul.get_letter_pos(upper) == emul.get_letter_pos(lower) == pos