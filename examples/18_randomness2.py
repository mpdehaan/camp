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
from camp.band.members.permit import Permit

def play():

    # in example 11 we showed off some random functionality
    # in example 17 we showed how to silence notes based on that
    # knowledge of 'random'.

    # here is a probabilistic way to use random, that combines the concepts.

    output = Performance(bpm=120, stop_seconds=15)

    source = ScaleSource(scales=scale("Ab blues"))

    melody = Roman(symbols=Endlessly("1 2 3 4 5 6 7".split()), channel=1)
    silence = Permit(when=Randomly([1, 0.5], mode='probability'))

    # so we're playing a scale pattern, but every other note has a 50% chance
    # of not being played.

    source.chain([melody, silence, output])
    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
