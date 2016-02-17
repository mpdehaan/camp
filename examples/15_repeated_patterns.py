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
from camp.band.selectors.repeatedly import Repeatedly
from camp.band.members.ordered import Ordered

def play():

    # in example 14 we showed how to nest patterns in ways that are easier
    # to conceptualize.  For instance, these patterns play in order, and we
    # call that a movement.  However, it's often tedious to specify things
    # that replay again and again.  To do make this easy, we have a new
    # selector to introduce - Repeatedly!


    output = Performance(bpm=240, stop_seconds=100)

    scale_choices = Endlessly([scale("D minor")])
    source = ScaleSource(scales=scale_choices)

    pattern1 = Roman(symbols=Repeatedly("1 2 3 4".split(), cycles=2))
    pattern2 = Roman(symbols="4 3 2 1".split())
    movement1 = Ordered(sources=[pattern1, pattern2])

    pattern3 = Roman(symbols=Repeatedly("1 4 1 4 1 5 1 5".split(), cycles=2))
    pattern4 = Roman(symbols="I IV V I".split())
    movement2 = Ordered(sources=[pattern3, pattern4])

    suite = Ordered(sources=[movement1, movement2], channel=1)

    source.send_to(suite)

    # for this example, we won't do anything crazy with transpositions or anything.

    suite.send_to(output)

    # BONUS TIP: we technically don't have to have just one conductor invocation, if it
    # keeps it simple.

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
