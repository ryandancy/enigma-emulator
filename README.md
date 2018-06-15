# Enigma Emulator

Emulates a German [Enigma machine][1] from World War 2.

Made as a project for Mr. Gillespie's CHC2DG class.

This project may be run using `python guiapp.py`.

To encrypt and decrypt using the Enigma emulator, start typing. The path each
letter's signal takes through the plugboard, rotors, and reflector is
represented by the green and red coloured wires. Note that due to the reflector,
the Enigma is reversible: type in some plaintext, write down the ciphertext,
hit "Reset", and type the ciphertext, and you will see that the original
plaintext appears.

The specific key that the Enigma machine is using can be changed using the
text inputs on the bottom.

The plugboard swaps (specific pairs of letters that
are swapped on input and output) can be changed by entering the pairs of letters
as a comma-separated list of Python 2-tuples containing those letters in the
first text box to the right of the Reset button. For
example, `('A', 'B'), ('F', 'G')` swaps A/B and F/G. Enter must be pressed when
you are done entering swaps.

The rotors (the three jumbles of wires in the middle of the screen, in which the
right-hand row of letters rotates on each letter press) can be changed using the
second text box to the right of the Reset button. There are eight rotors
available, named I through VIII. The three different rotors can be changed by
changing the list of rotors in the second text box. For example, to change the
first rotor to rotor VII, enter `'VII'` in place of `'III'` in the first string
in the list of three rotors in the second text box to the right and press enter.

The reflector (the reflecting jumble of wires on the right of the third rotor)
may also be changed between reflectors A, B, and C using the text box furthest
to the right. Simply change the prefilled `A` to `B` or `C` and press enter.

[1]: https://en.wikipedia.org/wiki/Enigma_machine