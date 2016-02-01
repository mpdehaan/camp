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

from functools import total_ordering

CHORD_TYPES = dict(
   minor = [ 3, 7 ],
   major = [ 4, 7 ],
   dim = [ 3, 6 ],
   aug = [ 4, 8 ]
)

from camp.core.note import note, Note

class Chord(object):

    def __init__(self, notes=None, root=None, typ=None):

        """
        Constructs a chord, in different ways:

        notes = [ note('C4'), note('E4'), note('G4') ]
	chord = Chord(notes=notes)

        OR:

        chord = Chord(root=note('C4'), type='major')

	OR:

	chord = Chord(root='C4', type='major')
        """

        self.notes = []
	
        if notes and root:
            raise Exception("notes= and root= are mutually exclusive")
        if notes is None and root is None:
            raise Exception("specify either notes= or root=")
        if root and typ is None:
            raise Exception("typ= is required when using root=")
        if typ and typ not in CHORD_TYPES:
            raise Exception("unknown chord type: %s, expecting one of: %s" % (typ, CHORD_TYPES))
        if isinstance(root, str):
            root = note(root) 

        if notes is not None:
            for x in notes:
                assert type(x) == Note
            self.notes = notes

        else:
            self.typ = typ
            self.root = root
            self.notes = self._chordify()
        

    def _chordify(self):
        """
        Internal method.
        Once self.root is set to a note, and self.typ is a chord type, like 'major', return the notes in the chord.
        """
        offsets = CHORD_TYPES[self.typ]
        notes = []
        notes.append(self.root)
        for offset in offsets:
            notes.append(self.root.transpose(semitones=offset)) 
        return notes

    def __repr__(self):
        """
        A chord prints like:
        Chord<C4,E4,G4>
        """
        note_list = ",".join([ n.short_name() for n in sorted(self.notes) ])
        return "Chord<%s>" % note_list

    def __eq__(self, other):
        """
        Chords are equal if they contain the same notes.
        """
        return sorted(self.notes) == sorted(other.notes)

    def transpose(self, steps=None, semitones=None, octaves=None):
        """
	Transposing a chord is returns a new chord with all of the notes transposed.
	"""
        notes = [ note.transpose(steps=steps, octaves=octaves, semitones=None) for note in self.notes ]
        return Chord(notes=notes)

def chord(input):
    """
    Shortcut: chord(['C5', 'E5', 'G5') -> Chord object
    Shortcut: chord('C5 dim') -> Chord object
    """
    if type(input) == list:
        notes = [ note(n) for n in input ]
        return Chord(notes)
    else:
        (root, typ) = input.split()
        return Chord(root=note(root), typ=typ)

