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
from camp.band.members.arp import Arp

from camp.band.selectors.endlessly import Endlessly

def play():

    # previous examples showed a couple of instruments, lets go back to one
    # instrument to showcase just the arpeggiator.

    # WARNING - may not make sense if you haven't used any hardware or
    # software arpeggiators.

    output = Performance(bpm=120, stop_seconds=10)

    scale1 = scale("c4 major")
    scale_choices = [ dict(scale=scale1, beats=7) ]

    # refresher - CAMP is generator based, and performances stop when there is
    # nothing left to do OR stop_seconds is reached.
    # by not wrapping the scale choices in "Endlessly", we're allowing this example
    # to terminate when the scale is done.  This example will play 24 quarter note
    # beats and STOP.  But the way the arpeggiator is coded, there will really be
    # 24*4 = 96 sixteenth notes, of which 3/4s of them will be played with audible notes
    # and the rests will be, ahem, rests.

    # refresher - the MIDI channel number can be set anywhere in the graph, as well as overrided
    # anywhere in the graph.  Leaving it off here on ScaleSource and setting it on the
    # Arp would do exactly the same thing.  Leaving off the channel will cause an exception.

    source = ScaleSource(scales=(scale_choices), channel=1)

    # refresher - the scale follower will take note of the current scale and
    # play the scale for a given number of notes in order.  We could be more
    # creative by using Roman() instead to select particular notes (or chords)
    # in the scale.

    follower = ScaleFollower(lengths=Endlessly([7]))

    # refresher, the roman usage looks very similar:
    # roman = Roman(symbols="1 2 3 4 5 6 7".split())
    # really, there's little use for ScaleFollower in the real world, but it was
    # getting lonely and wanted to be featured here.  It's a bit more efficient
    # but I doubt that matters.

    # NOW FOR THE FUN PART.

    # ok, here's the arpeggiator.

    # in this example, we take the currently selected note from the scale
    # play that note, then the notes 4 and 9 semitones up - a major chord.
    # every single beat will be divided into 4 parts by the arp due to 'splits'
    # however every 4th note is also a REST.
    #
    # see this table:
    #
    # TRIGGER: | C4 ~~~~~~~~~~~~ | D4 ~~~~~~~~~ | ...
    # ---------+-----------------+--------------+
    # RESTS:   | N   N   N  Y    | N   N   N  Y |
    # SEMI:    | +0  +3  +8  -   | +0  +3  +8   |
    # OCTAVES: | +2  -2  0   0   | +2  -2  0  0 |
    # ---------+-----------------+--------------+
    # PLAY:    | C6  E2  G4  -   | D6  Gb2 A4 - |
    #
    # more creative things can be done by having the semitones
    # and rest patterns be different lengths, and so on, as well as using
    # the 'free' mode with those uneven lengths.

    arp = Arp(
        semitones=Endlessly([0,3,8,0]),
        octaves=Endlessly([2,-2,0,0]),
        splits=Endlessly([4]),
        rests=Endlessly([0,0,0,1])
    )

    # HOMEWORK: add "mode=free" to the Arp constructor above and experiment
    # with octaves, splits, rests, and semitones of different values and array
    # lengths.

    # POP QUIZ:  what happens if we remove Endlessly from some of the expressions above?
    # WHY?

    # the chain here is simple - scale source feeds note source, which in turn
    # feeds the arp.

    source.chain([follower, arp, output])

    # kick out the jams

    conductor = Conductor(signal=[source], performance=output)
    conductor.start()


if __name__ == "__main__":
    play()
