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
from camp.core.chord import chord
from camp.core.scale import scale
from camp.notation.roman import Roman, roman
from camp.notation.literal import Literal

class TestRoman(object):

    def test_basics(self):

        r = Roman(scale=scale("C4 major"))

        assert r.do("1") == note("C4")
        assert r.do("3") == note("E4")
        assert r.do("4") == note("F4")

        assert r.do("IV") == chord("F4 major")
        assert r.do("iv") == chord("F4 minor")

        # somewhat non-standard notation but allows describing other chord types (see chord.py)
        assert r.do("I:power") == chord(["C4", "G4"])

    def test_shortcuts(self):

        r = roman("C4 major")
        assert r.do("IV") == chord("F4 major")

    def test_inversions(self):

        # non-standard notation but I wanted a somewhat clean-ish way to describe inversions
        r = roman("C4 major")
        assert r.do("I'")  == chord(["E4","G4","C5"])
        assert r.do("I''") == chord(["G4","C5","E5"])
        assert r.do("I':power") == chord(["G4","C5"])

class TestLiteral(object):

    def test_basics(self):

        l = Literal()
        assert l.do("C4") == note("C4")
        assert l.do("C4-major") == chord("C4 major")
        assert l.do("C4,E4,G4") == chord("C4 major")

        # FIXME: inversions are not supported in literal.py yet, we'd ideally want
        # this in a common base class -- low priority
        #assert l.do("C4'-major") == chord("C5,E4,G4")
