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


def play():

    output = Performance(bpm=120, stop_seconds=10)

    scale1 = scale("c6 major")
    scale2 = scale("c6 minor")

    # the performance will use the c6 major scale for 7 beats, then the c6 minor scale for 7 beats
    source = ScaleSource(scales=[ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ])

    # the scale follower will play the first 7 notes in each scale
    follower = ScaleFollower(lengths=[7, 7], channel=1)

    source.chain([follower, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
