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
from camp.band.members.subdivide import Subdivide
from camp.band.members.chordify import Chordify
from camp.band.members.scale_follower import ScaleFollower
from camp.band.members.transpose import Transpose


class TestBand(object):

    def test_new_api(self):
        # realtime = Realtime()
        # timeline = Timeline()
        output = Performance(bpm=120, stop_seconds=10)

        scale1 = scale("c6 major")
        scale2 = scale("c6 minor")

        source = ScaleSource(scales=[ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ])

        subdivide = Subdivide(splits=[4])
        roman = Roman(symbols="1 2 3 4 I IV V iii".split(), channel=1)

        follower = ScaleFollower(lengths=[ 7 ])
        chordify = Chordify(types=[ 'power' ])
        shift = Transpose(octaves=[-3], channel=2)

        source.chain([subdivide, roman, output])
        source.chain([follower, chordify, shift, output])


        conductor = Conductor(signal=[source], performance=output)
        conductor.start()
