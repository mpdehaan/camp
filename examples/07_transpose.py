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

from camp.band.selectors.endlessly import Endlessly

def play():

    # example 05 was "playing all the power chords in a chromatic scale".
    # example 06 used subdivide to chop up alternating measures with faster notes
    # now lets alternately transpose every 2nd measure up an octave
    # and every 3rd measure down an octave

    output = Performance(bpm=120, stop_seconds=10)

    source = ScaleSource(scales=scale("c4 chromatic"))

    follower = ScaleFollower(lengths=Endlessly([12]))

    subdivide = Subdivide(splits=Endlessly([1,4]))

    # pay attention to this part - nothing else has changed
    transpose = Transpose(octaves=Endlessly([0,1,-1]))

    chordify = Chordify(types="power", channel=1)
    source.chain([follower, subdivide, transpose, chordify, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
