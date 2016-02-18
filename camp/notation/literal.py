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

class Literal(object):

    def __init__(self, scale=None):

        """
        Constructs an interpreter for specific note names or chords.
        It doesn't need to know a scale and is pretty basic.

	    literal = Literal()
        roman.do("C4,E4,G4") == chord("C4 major")
        roman.do("C4 major") == chord("C4,E4,G4")
        roman.do("C4") == note("C4")
        """
        pass

    def do(self, sym):
        """
        Accepts symbols like C4-major or C4,E4,G4
        or note symbols like 'C4'
        """
        # The dash is a bit of a notation hack, it's there because "C4 major"
        # would look like two symbols, so we need to have no whitespace
        # between them

        if sym is None or sym == '-':
            # REST:
            return chord([])
        if '-' in sym:
            return chord(sym.replace("-"," "))
        elif "," in sym:
            return chord(sym.split(","))
        else:
            return note(sym)

    def do_notes(self, sym):
        """
        Same as do() but always get back an array of notes.
        """
        # DRY: duplication with Roman.py - FIXME
        if sym == '-':
            # REST
            return []
        note_or_chord = self.do(sym)
        if note_or_chord is None:
            return []
        elif type(note_or_chord) == Chord:
            return note_or_chord.notes
        else:
            return [ note_or_chord ]



def literal():
    """
    The shortcut method here isn't highly useful, but it's being provided
    to line up with the REST of the API.
    """
    return Literal()
