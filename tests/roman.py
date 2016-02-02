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
from camp.systems.roman import Roman

class TestRoman(object):

   def test_basics(self):

       roman = Roman(scale=scale("C4 major"))

       assert roman.do("1") == note("C4")
       assert roman.do("3") == note("E4")
       assert roman.do("4") == note("F4")

       assert roman.do("IV") == chord("F4 major")
       assert roman.do("iv") == chord("F4 minor")
       assert roman.do("I:power") == chord(["C4", "G4"])
