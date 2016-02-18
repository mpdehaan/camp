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

from camp.core.note import note
from camp.core.chord import Chord, chord

class TestChord(object):

   def test_basics(self):

       notes = [ note('C4'), note('E4'), note('G4')]

       chord1 = Chord(notes=notes)
       assert chord1.notes[0] == note('C4')
       assert chord1.notes[1] == note('E4')
       assert chord1.notes[2] == note('G4')
       assert str(chord1) == 'Chord<C4,E4,G4>'

       chord2 = chord(['G4','C4','E4'])
       assert str(chord2) == 'Chord<C4,E4,G4>'
       assert chord1 == chord2

       assert chord(['C4','E4','G4']) != chord(['C4'])
       assert chord(['C4','E4','G4']) != chord(['C4', 'E4', 'G4', 'C5'])

   def test_chord_types_and_shortcuts(self):

       assert Chord(root=note('C4'), typ='major') == chord(['C4', 'E4', 'G4'])
       assert Chord(root=note('C4'), typ='minor') == chord(['C4', 'Eb4', 'G4'])

       assert chord('C4 major') == chord(['C4', 'E4', 'G4'])
       assert chord('C major') == chord(['C4', 'E4', 'G4'])
       assert chord('C aug') == chord(['C4', 'E', 'Ab4'])
       assert chord('C dim') == chord(['C4', 'Eb4', 'Gb4'])

   def test_transpose(self):

       chord1 = chord(['G4','C4','E4'])
       assert chord1.transpose(steps=0.5) == chord(['Db4', 'F4', 'Ab4'])
       assert chord1.transpose(octaves=2) == chord(['C6', 'E6', 'G6'])

   def test_inversions(self):
       assert chord("C4 major").invert() == chord(["E4","G4","C5"])
       assert chord("C4 major").invert(amount=2) == chord(["G4","C5","E5"])
