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
from camp.band.members.transpose import Transpose
from camp.band.members.scale_follower import ScaleFollower
from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.randomly import Randomly
from camp.band.members.ordered import Ordered

def play():

    # in example 13 we showed the use of Ordered to trigger
    # one pattern after another.  As programs grow, it might be nice
    # to group them conceptually in a larger composition.

    # This is a demo that shows how Ordered can nest to not work only
    # with basic patterns, but also larger movements.

    # The idea is this: Generators stack!

    # Like before, we're setting stop seconds to 100 seconds but this composition
    # will complete due to the sources being exhausted first, which is the point.


    output = Performance(bpm=240, stop_seconds=100)

    for scale_name in ["C major", "D minor"]:

        scale_choices = Endlessly([scale(scale_name)])
        source = ScaleSource(scales=scale_choices)

        pattern1 = Roman(symbols="1 2 3 4 5 6 7".split())
        pattern2 = Roman(symbols="i ii iii iv v v vii".split())
        movement1 = Ordered(sources=[pattern1, pattern2])

        pattern3 = Roman(symbols="7 6 5 4 3 2 1".split())
        pattern4 = Roman(symbols="vii vi v iv iii ii i".split())
        movement2 = Ordered(sources=[pattern3, pattern4])
        movement2_transposer = Transpose(octaves=Endlessly([-2]))
        movement2.send_to(movement2_transposer)

        suite = Ordered(sources=[movement1, movement2], channel=1)

        source.send_to(suite)
        output.listens_to([movement1, movement2_transposer])

        # BONUS TIP: we technically don't have to have just one conductor invocation, if it
        # keeps it simple.

        conductor = Conductor(signal=[source], performance=output)
        conductor.start()


if __name__ == "__main__":
    play()
