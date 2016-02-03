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
from camp.opus.song import Song
from camp.opus.scene import Scene
from camp.opus.track import Track
from camp.opus.pattern import Pattern

class TestSong(object):

    def test_basic_api_usage(self):

        # this test is mostly documentation and coverage and is going to be
        # relatively free of assertions, because of the nature of the work

        # the opus is the framework for a composition.  It has a Python object
        # model which is also the basic API.  At a high level:
        # a song has tracks
        # a song has scenes
        # each scene chooses a pattern for each track
        # a scene might override the scale or BPM
        # each pattern has bars (which might repeat)
        # bars can be described in multiple types of systems
        # a pattern might override the scale (but can't override the BPM)
        # scenes might be manually advanced by a human, or they might not.

        # values set at the song level are essentially global defaults
        song = Song(name="Random Notes", scale=scale('c4 major'), pattern_length=16, bars=4, bpm=120)

        # tracks get mapped to MIDI channels but they also have printable names
        track1 = song.add_track(Track(name="melodica", midi_channel=1))
        track2 = song.add_track(Track(name="trombone", midi_channel=2))
        track3 = song.add_track(Track(name="TR808", midi_channel=2))

        # a pattern has a name, a notation system, and can optionally override a scale
        llama_pattern = Pattern(name="llama-theme", notation='roman', scale=scale('c4 minor'),
            bars = [
               "1 2 3 I II III IV i ii iii iv - 3 2 1".split(),
            ]
        )
        # here the pattern plays the first bar 3 times then the next bar 1 time
        sheep_pattern = Pattern(name="sheep-theme", notation='roman',
            bars = [
                "4 6 4 6 4 4 4 4 6 6 4 1 1 - - - -".split(),
                "4 6 4 6 4 4 4 4 6 4 6 1 . . . . ."
            ],
            bar_repeats = [ 3, 1 ]
        )
        # for drums, scales are pretty bogus, so just input the raw notes (or chords, etc)
        kick_pattern = Pattern(name="kicks", notation='literal', bars=["C4 - - -".split()], stop=4)

        # the song has a list of scenes, which might repeat
        scene1 = song.add_scene(Scene(name="scene1", track_mapping=dict(
            track1 = llama_pattern,
            track2 = sheep_pattern,
            track3 = kick_pattern
        )))

        # scenes can also override many of the global settings
        scene2 = song.add_scene(Scene(name="scene2", scale=scale('c5 minor'), bpm=140, bars=6, track_mapping=dict(
            track1 = llama_pattern,
            track2 = sheep_pattern,
            track3 = None
        )))

        # PSEUDOCODE SKETCH: TODO: real-time AND rendering will probably look like:
        # while True
        #     sleep(SMALL_NUMBER) # unless rendering
        #     events = song.advance_time(SMALL_NUMBER)
        #     for x in events
        #        send or print event
        # ??? - to be determined
