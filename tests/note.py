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

class TestNote(object):

   def test_comparisons(self):

       for nm in NOTES:
           assert Note(name=nm, octave=4) > Note(name=nm, octave=3)

       for nm in [ 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'Bb' ]:
          assert Note(name=nm, octave=4) > Note(name='C', octave=4)
          assert Note(name=nm, octave=3) < Note(name='C', octave=4)


   def test_transpose(self):

       # half steps (+)
       assert Note(name='C', octave=4).transpose(steps=0.5)  == Note(name='Db', octave=4)
       assert Note(name='Db', octave=4).transpose(steps=0.5) == Note(name='D', octave=4)
       assert Note(name='D', octave=4).transpose(steps=0.5)  == Note(name='Eb',  octave=4)
       assert Note(name='Eb', octave=4).transpose(steps=0.5) == Note(name='E', octave=4)
       assert Note(name='E', octave=4).transpose(steps=0.5)  == Note(name='F',  octave=4)
       assert Note(name='F', octave=4).transpose(steps=0.5)  == Note(name='Gb',  octave=4)
       assert Note(name='Gb', octave=4).transpose(steps=0.5) == Note(name='G', octave=4)
       assert Note(name='G', octave=4).transpose(steps=0.5)  == Note(name='Ab',  octave=4)
       assert Note(name='Ab', octave=4).transpose(steps=0.5) == Note(name='A', octave=4)
       assert Note(name='A', octave=4).transpose(steps=0.5)  == Note(name='Bb',  octave=4)
       assert Note(name='Bb', octave=4).transpose(steps=0.5) == Note(name='B', octave=4)
       assert Note(name='B', octave=4).transpose(steps=0.5)  == Note(name='C',  octave=5)

       # whole steps (+) 
       assert Note(name='C', octave=4).transpose(steps=1)  == Note(name='D',  octave=4)
       assert Note(name='Db', octave=4).transpose(steps=1) == Note(name='Eb', octave=4)
       assert Note(name='D', octave=4).transpose(steps=1)  == Note(name='E',  octave=4)
       assert Note(name='Eb', octave=4).transpose(steps=1) == Note(name='F',  octave=4)
       assert Note(name='E', octave=4).transpose(steps=1)  == Note(name='Gb', octave=4)
       assert Note(name='F', octave=4).transpose(steps=1)  == Note(name='G',  octave=4)
       assert Note(name='Gb', octave=4).transpose(steps=1) == Note(name='Ab', octave=4)
       assert Note(name='G', octave=4).transpose(steps=1)  == Note(name='A',  octave=4)
       assert Note(name='Ab', octave=4).transpose(steps=1) == Note(name='Bb', octave=4)
       assert Note(name='A', octave=4).transpose(steps=1)  == Note(name='B',  octave=4)
       assert Note(name='Bb', octave=4).transpose(steps=1) == Note(name='C',  octave=5)
       assert Note(name='B', octave=4).transpose(steps=1)  == Note(name='Db', octave=5)

       # octaves (+)
       assert Note(name='C', octave=3).transpose(octaves=2)  == Note(name='C', octave=5)

       # half steps (-)
       assert Note(name='C', octave=4).transpose(steps=-0.5)  == Note(name='B',  octave=3)
       assert Note(name='Db', octave=4).transpose(steps=-0.5) == Note(name='C',  octave=4)
       assert Note(name='D', octave=4).transpose(steps=-0.5)  == Note(name='Db', octave=4)
       assert Note(name='Eb', octave=4).transpose(steps=-0.5) == Note(name='D',  octave=4)
       assert Note(name='E', octave=4).transpose(steps=-0.5)  == Note(name='Eb', octave=4)
       assert Note(name='F', octave=4).transpose(steps=-0.5)  == Note(name='E',  octave=4)
       assert Note(name='Gb', octave=4).transpose(steps=-0.5) == Note(name='F',  octave=4)
       assert Note(name='G', octave=4).transpose(steps=-0.5)  == Note(name='Gb', octave=4)
       assert Note(name='Ab', octave=4).transpose(steps=-0.5) == Note(name='G',  octave=4)
       assert Note(name='A', octave=4).transpose(steps=-0.5)  == Note(name='Ab', octave=4)
       assert Note(name='Bb', octave=4).transpose(steps=-0.5) == Note(name='A',  octave=4)
       assert Note(name='B', octave=4).transpose(steps=-0.5)  == Note(name='Bb', octave=4)

       # whole steps (-)
       assert Note(name='C', octave=4).transpose(steps=-1)  == Note(name='Bb', octave=3)
       assert Note(name='Db', octave=4).transpose(steps=-1) == Note(name='B',  octave=3)
       assert Note(name='D', octave=4).transpose(steps=-1)  == Note(name='C',  octave=4)
       assert Note(name='Eb', octave=4).transpose(steps=-1) == Note(name='Db', octave=4)
       assert Note(name='E', octave=4).transpose(steps=-1)  == Note(name='D',  octave=4)
       assert Note(name='F', octave=4).transpose(steps=-1)  == Note(name='Eb', octave=4)
       assert Note(name='Gb', octave=4).transpose(steps=-1) == Note(name='E',  octave=4)
       assert Note(name='G', octave=4).transpose(steps=-1)  == Note(name='F',  octave=4)
       assert Note(name='Ab', octave=4).transpose(steps=-1) == Note(name='Gb', octave=4)
       assert Note(name='A', octave=4).transpose(steps=-1)  == Note(name='G',  octave=4)
       assert Note(name='Bb', octave=4).transpose(steps=-1) == Note(name='Ab', octave=4)
       assert Note(name='B', octave=4).transpose(steps=-1)  == Note(name='A',  octave=4)
       
       # octaves (-)
       assert Note(name='C', octave=3).transpose(octaves=-2)  == Note(name='C', octave=1)

       # amrbitrary hops
       assert Note(name='C', octave=4).transpose(2.5)        == Note(name='F', octave=4)
       assert Note(name='F', octave=4).transpose(-2.5)       == Note(name='C', octave=4) 
       assert Note(name='F', octave=4).transpose(-3.0)       == Note(name='B', octave=3)
       assert Note(name='C', octave=4).transpose(7)          == Note(name='D', octave=5)


   def test_equivalence(self):

       assert Note(name='Db', octave=4) == Note(name='C#', octave=4)
       assert Note(name='Eb', octave=4) == Note(name='D#', octave=4)
       assert Note(name='Gb', octave=4) == Note(name='F#', octave=4)
       assert Note(name='Ab', octave=4) == Note(name='G#', octave=4)
       assert Note(name='Bb', octave=4) == Note(name='A#', octave=4)

   def test_shortcuts(self):
  
       assert note("C")   == Note(name="C", octave=4)
       assert note("Db3") == Note(name="Db", octave=3)
       assert note("Db")  == Note(name="Db")
       assert note("D#5") == Note(name="Eb", octave=5)
       assert note("D#")  == Note(name="Eb", octave=4)

