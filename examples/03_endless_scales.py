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

from camp.band.selectors.endlessly import Endlessly

def play():

    # this really isn't endless, because we've engaged a global stop timer.
    # but if you change 10 to 100, it will play for 100 seconds.  Make note
    # of the use of Endlessly here to see that data sources are not exhausted.

    output = Performance(bpm=120, stop_seconds=10)

    # play the two scales for 7 beats each, and then keep using those scales
    scale1 = scale("c6 major")
    scale2 = scale("c6 minor")
    scale_choices = [ dict(scale=scale1, beats=7), dict(scale=scale2, beats=7) ]

    source = ScaleSource(scales=Endlessly(scale_choices))

    # note: the syntax is simpler to just play ONE scale repeatedly, and you'll see this
    # done more in future examples.  Because we don't need to stay in one scale for N beats
    # before moving on to another, we don't need all the extra info.
    # source = ScaleSource(scales=scale1)

    # the scale follower will play the first 7 notes in each scale, whatever the current
    # scale is.
    follower = ScaleFollower(lengths=7, channel=1)
    source.chain([follower, output])

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()

if __name__ == "__main__":
    play()
