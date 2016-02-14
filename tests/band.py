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
from camp.band.subdivide import Subdivide
from camp.band.chordify import Chordify
from camp.band.realtime_output import RealtimeOutput
from camp.band.conductor import Conductor

class TestBand(object):

    def test_mesh_basic(self):

        realtime = Realtime()
        timeline = Timeline()

        scale1 = scale("c6 major")
        scale2 = scale("c6 minor")
        scale3 = scale("c3 minor")

        scale_reader_track1 = ScalePlayer(scales=[scale1, scale2], lengths=[16,4], channel=0, note_velocities=[127,80,50])
        subdivide_track1 = Subdivide(amounts=[4])
        scale_reader_track1.send_to(subdivide_track1)

        scale_reader_track2 = ScalePlayer(scales=[scale3], lengths=[16,4], channel=0, note_velocities=[127])
        chordify_track2 = Chordify(types=['major','minor'], channel=0)
        scale_reader_track2.send_to(chordify_track2)

        output = RealtimeOutput(timeline=timeline, bpm=120, time_boredom_seconds=5)
        subdivide_track1.send_to(output)
        chordify_track2.send_to(output)

        #chordify.send_to(output)

        # FIXME: BUG: time_boredom_seconds does not appear to work.
        # FIXME: BUG: if multiple outputs are in the list, one slows down the other.  They should not.

        conductor = Conductor(
            #signal=[scale_reader_track1, scale_reader_track2],
            signal=[scale_reader_track1],

            output=output,
            realtime=realtime,
            timeline=timeline,
            output_modes=['play_events','print_events','save_events'])

        conductor.start()

        for x in conductor.midi_event_buffer:
            print(x)
