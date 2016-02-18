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
from camp.band.members.literal import Literal
from camp.band.selectors.endlessly import Endlessly
from camp.band.members.velocity import Velocity

def play():

    # 21 examples an no mention of velocity (loudness) yet?  Wow.
    # velocity is easy.  in MIDI, velocity is a loudness level from 127 (maximum)
    # to 0 (silent).

    # because the human ear percieves different pitches at different loudnesses,
    # the following is a silly demo of repeating a middle C at different loudness
    # levels.

    # (IDEA: this gives me the idea for a math-equation type iterator so I can do sine
    # curves for various automation, but... later)

    output = Performance(bpm=120, stop_seconds=15)

    melody = Literal(symbols=Endlessly(["C4"]), channel=1)
    velocity = Velocity(levels=Endlessly([10,20,30,40,50,60,70,80,90,100,110,120]))

    melody.chain([velocity, output])
    conductor = Conductor(signal=[melody], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
