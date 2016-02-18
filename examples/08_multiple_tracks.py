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
from camp.band.members.subdivide import Subdivide
from camp.band.members.transpose import Transpose
from camp.band.members.roman import Roman

from camp.band.selectors.endlessly import Endlessly

def play():

    # here's an example that might *START* to approximate a song.
    # here we have two instruments playing on two different tracks.

    output = Performance(bpm=120, stop_seconds=10)

    # both instruments will use the same scale at the same time, but there is a scale
    # change as we cycle between scales every 24 beats

    scale1 = scale("c5 major_pentatonic")
    scale2 = scale("e5 mixolydian")
    scale_choices = [ dict(scale=scale1, beats=24), dict(scale=scale2, beats=24) ]
    source = ScaleSource(scales=Endlessly(scale_choices))

    # the first instrument plays a series of chords, transposed down an octave
    # from the original scale carrier signal.

    roman1 = Roman(symbols=Endlessly("I IV V IV III:dim ii".split()), channel=1)
    transpose1 = Transpose(octaves=-1)
    source.chain([roman1,transpose1,output])

    # the second instrument plays a series of notes, but is responding to sixteenth
    # notes, not quarter notes, because of the subdivide.

    subdivide2 = Subdivide(splits=4)
    roman2 = Roman(symbols=Endlessly("1 4 3 4 4 3 2 1".split()), channel=2)
    source.chain([subdivide2,roman2,output])

    # homework assignment:
    # change subdivide2 so it's chained BEFORE roman2
    # what happens and why?

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
