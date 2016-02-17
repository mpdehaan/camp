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

from camp.core.scale import scale
from camp.band.conductor import Conductor

from camp.band.members.performance import Performance
from camp.band.members.scale_source import ScaleSource
from camp.band.members.roman import Roman
from camp.band.selectors.endlessly import Endlessly
from camp.band.members.chordify import Chordify
from camp.band.members.arp import Arp

def play():

    # here we aren't introducing any new concepts, but we're arranging some
    # concepts a little differently.  This is somewhat of a review, as we're going
    # to start exploring some more (hopefully) musical demos in our examples now.

    # This one sounds just a bit Perrey and Kingsley with the right VST.

    output = Performance(bpm=120, stop_seconds=10)

    # let's play in the A major scale

    scale_choices = Endlessly(
        [
            dict(scale=scale("a4 major"))
        ]
    )

    source = ScaleSource(scales=scale_choices)

    # we're going to alternate between the 1st, 4th, and 5th notes
    # of the scale, but we didn't just jump to chords because of what
    # we are about to do with the arp.

    roman = Roman(symbols=Endlessly("1 4 5".split()), channel=1)

    # and now for a clever use of the arp, to machine gun 4 repititions of
    # each chord, with rests in between.  Subdivide alone couldn't do this.
    # Also notice this is running with NO tranpositions.

    arp = Arp(
        # no transpositions
        semitones=Endlessly([0,0,0,0,0,0,0,0]),
        # every beat gets sliced up 8 times, no exceptions
        splits=Endlessly([8]),
        # try uncommenting this next line:
        #octaves=Endlessly([0,0,1,0,2,0,3,0]),
        # play every other note on the arp
        # TODO: IDEA: seems like we should also allow arp velocity!
        rests=Endlessly([0,1,0,1,0,1,0,1])
    )

    # now the output here is just machine gunned notes.  Turn it into major chords.

    chordify = Chordify(types=Endlessly(['major']))

    source.chain([roman, arp, chordify, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
