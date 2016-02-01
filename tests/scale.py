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

from camp.core.note import Note, NOTES, note
from camp.core.chord import Chord, chord
from camp.core.scale import Scale, scale

class TestScale(object):

   def test_basics(self):

       scale1 = Scale(root=note('C4'), typ='major')
       scale2 = scale('C4 major')
       assert scale1 == scale2
       assert str(scale1) == 'Scale<C4 major>'

   def test_c_major(self):

       scale1 = scale('C4 major')
       results = []
       for note in scale1.generate(length=10):
           results.append(note)
   
       # using chords here is kind of silly but it's a useful test function
       # naturally you wouldn't play it this way
       assert chord(results) == chord(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5'])

