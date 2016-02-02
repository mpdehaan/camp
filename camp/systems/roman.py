"""
Copyright 2016, Michael DeHaan <michael.dehaan@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from camp.core.note import note, Note
from camp.core.chord import chord, Chord
from camp.core.scale import scale, Scale

CHORD_SYMBOLS = dict(
   I   = [ 1, 'major' ],
   II  = [ 2, 'major' ],
   III = [ 3, 'major' ],
   IV  = [ 4, 'major' ],
   V   = [ 5, 'major' ],
   VI  = [ 6, 'major' ],
   VII = [ 7, 'major' ],
   i   = [ 1, 'minor' ],
   ii  = [ 2, 'minor' ],
   iii = [ 3, 'minor' ],
   iv  = [ 4, 'minor' ],
   v   = [ 5, 'minor' ],
   vi  = [ 6, 'minor' ],
   vii = [ 7, 'minor' ],   
)

class Roman(object):

    def __init__(self, scale=None):

        """
        Constructs an interpreter for Roman numbering.

        scale1 = scale("C4 major")
	roman = Roman(scale=scale1)
        roman.do("IV") == chord("F4 major")
        roman.do(4) == note("F4")
        """

        assert scale is not None
        self.scale = scale

        self._note_buffer = [ n for n in self.scale.generate(length=20) ]

    def chord(self, sym):
        """
        Accepts symbols like ii, II, IV:power
        (the latter being a bit of a notation hack so we might want to change it)
        """
 
        override_typ = None
        if ":" in sym:
           (sym, override_typ) = sym.split(":",1)

        chord_data = CHORD_SYMBOLS.get(sym, None)
        if chord_data is None:
           raise Exception("do not know how to parse chord symbol: %s" % sym)

        (scale_num, typ) = chord_data
        if override_typ is not None:
            typ = override_typ
        base_note = self.note(scale_num)
        return Chord(root=base_note, typ=typ)

    def note(self, sym):
        position = int(sym) - 1
        return self._note_buffer[position]

    def do(self, sym):
        """
        Generate a note from a symbol like '2', or a chord from a symbol like
        'ii' or 'II'.
        """
        try:
            int(sym)
        except ValueError:
            return self.chord(sym)
        return self.note(sym)

def roman(scale_pattern):
    """
    Quickly generate a Roman numeral interpreter.
    Ex: r = roman("C4 major")
    """
    return Roman(scale=scale(scale_pattern))


