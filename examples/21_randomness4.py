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
from camp.band.selectors.randomly import Randomly
from camp.band.members.chordify import Chordify
from camp.band.members.permit import Permit
from camp.band.members.transpose import Transpose

def play():

    # we've focussed a lot on randomness now.  So far, we've shown how to pick random values
    # for notes and how to conditionally do something or not with "when=".

    # What's interesting though is that, due to the way some effects plugins work, we can choose
    # to intermix effects.  Here, we show that there are really two patterns going on, but only one
    # is going to win and actually get to play a note.

    # we're relying one 'musician' object stomping on another, but only sometimes.

    output = Performance(bpm=120, stop_seconds=15)

    source = ScaleSource(scales=scale("Ab blues"))

    pattern1 = Endlessly("1 2 3 4 5 6 7".split())
    pattern2 = Randomly("VII:power VI:power V:power IV:power III:power II:power I:power".split())
    cut_over = Randomly([0,0,0,1,1,1], mode='probability')

    melody1 = Roman(symbols=pattern1, channel=1)
    melody2 = Roman(symbols=pattern2, channel=2, when=cut_over)
    transpose = Transpose(octaves=Endlessly([-2,-1,0,1,2]))

    # there is no sane reason to want to do this, but what happens is that for the first three notes we are guaranteed
    # to play pattern1.  Then three notes of pattern 2.  The last note is acutally a toss up between pattern1 and pattern2.
    # since they live in the same chain, pattern1 is going to overwrite pattern2 even though they are expressed in a chain.
    # we can also even choose to overwrite the MIDI channel, which we do, all while sharing a transposition cycle.

    # again, this isn't realistic for most compositions, we'd likely just set up a bunch of patterns with RESTS, but
    # I wanted to show all the possibilities before leaving the theme of randomness for a while.  Hopefully the
    # idea of "when=" is now drummed in.

    source.chain([melody1, melody2, transpose, output])
    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
