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
from camp.playback.realtime import Realtime
from camp.playback.timeline import Timeline
from camp.band.scale_player import ScalePlayer
from camp.band.roman_player import RomanPlayer
from camp.band.subdivide import Subdivide
from camp.band.chordify import Chordify
from camp.band.realtime_output import RealtimeOutput
from camp.band.conductor import Conductor

class TestBand(object):

    COMMENTS = """
    def test_mesh_one(self):

        realtime = Realtime()
        timeline = Timeline()

        scale1 = scale("c6 major")
        scale2 = scale("c6 minor")
        scale3 = scale("c3 minor")
        scale4 = scale("c4 major")

        subdivide_track1 = Subdivide(amounts=[2,4,8])
        scale_reader_track1 = ScalePlayer(scales=[scale1, scale2], lengths=[16,4], note_durations=[0.25], channel=1, note_velocities=[127,80,50])
        subdivide_track1.send_to(scale_reader_track1)

        scale_reader_track2 = ScalePlayer(scales=[scale3, scale4], lengths=[4,4], note_durations=[1], channel=2, note_velocities=[127])
        chordify_track2 = Chordify(types=['major'], channel=0)
        scale_reader_track2.send_to(chordify_track2)

        output = RealtimeOutput(timeline=timeline, bpm=120, time_boredom_seconds=10)
        scale_reader_track1.send_to(output)
        chordify_track2.send_to(output)

        conductor = Conductor(
            signal=[subdivide_track1, scale_reader_track2],
            output=output,
            realtime=realtime,
            timeline=timeline)

        conductor.start()
    """

    #MEH = """
    def test_mesh_roman(self):

        realtime = Realtime()
        timeline = Timeline()

        # play a C major scale for 12 notes on channel 1, repeating, with consistently maximally loud quarter notes each time
        scale_reader_track1 = ScalePlayer(scales=[scale("c4 major")], lengths=[12], note_durations=[0.25], channel=1, note_velocities=[127])
        # except throw away the scale and just note what scale we are playing (the same one, here)
        # and use roman numeral notation to decide what we are really playing - a mix of notes and chords in that scale
        roman_player_track1 = RomanPlayer(symbols="1 2 3 4 I IV V iii".split(), channel=1)
        # FIMXE: TODO: this really makes RomanPlayer a type of Middleware - maybe we want to represent that as ScaleMiddleware and rename it.
        # Chordify is also like that.  Then rename ScalePlayer to ScaleReader.
        scale_reader_track1.send_to(roman_player_track1)

        # we'll play that and only that for 5 seconds
        output = RealtimeOutput(timeline=timeline, bpm=120, time_boredom_seconds=5)
        roman_player_track1.send_to(output)

        conductor = Conductor(
            signal=[scale_reader_track1],
            output=output,
            realtime=realtime,
            timeline=timeline)

        conductor.start()
    #"""
