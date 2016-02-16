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
from camp.band.members.scale_follower import ScaleFollower
from camp.band.members.chordify import Chordify
from camp.band.members.subdivide import Subdivide
from camp.band.members.transpose import Transpose
from camp.band.members.roman import Roman

from camp.band.selectors.endlessly import Endlessly

def play():

    # this is sort of a variation of example 08.  Except now, rather than
    # playing two different patterns that might clash, we're selecting chord
    # patterns for instrument 2 to harmonize with what instrument 1 is playing.

    output = Performance(bpm=120, stop_seconds=10)

    # both instruments will use the same scale at the same time, but there is a scale
    # change as we cycle between scales every 24 beats

    scale1 = scale("c5 major_pentatonic")
    scale2 = scale("e5 mixolydian")
    scale_choices = [ dict(scale=scale1, beats=24), dict(scale=scale1, beats=24) ]
    source = ScaleSource(scales=Endlessly(scale_choices))

    # the first instrument plays a series of chords, transposed down an octave
    # from the original scale carrier signal.

    roman1 = Roman(symbols=Endlessly("1 2 4 1 2 3 1 2 4 3 3".split()), channel=1)
    source.chain([roman1, output])

    chordify = Chordify(types=Endlessly("major major major minor".split()), channel=2)
    transpose = Transpose(octaves=Endlessly([-2]))
    source.chain([roman1, chordify, transpose])

    # note that roman 1 is part of each chain, but the channel number is overridden
    # in the second set.  This can be done because the event objects are copied as they
    # are passed between each layer.  Technically the channel can be overriden at any
    # time.  Ideas for future chaos, perhaps?

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
