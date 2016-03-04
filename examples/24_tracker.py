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

from camp.tracker.song_factory import SongFactory
from camp.tracker.defaults import Defaults
from camp.tracker.instruments import Instruments
from camp.tracker.instrument import Instrument
from camp.tracker.patterns import RandomPatterns, BasicPatterns, EndlessPatterns
from camp.tracker.fx_buses import FxBuses
from camp.tracker.fx_bus import FxBus
from camp.tracker.scenes import Scenes
from camp.tracker.scene import Scene

# ---------------------------------------------------------------------------------
# WARNING -- THIS EXAMPLE IS UNDER DEVELOPMENT CURRENTLY
# AND IS NOT YET OPERATIONAL.  This also applies to the whole camp.tracker
# namespace.

# One possible next step after this is to build the generative API *on top* of the Tracker API
# as this manages instrument routing for us and is therefore easier to think about
#
# We'll probably build a ASCII TUI sequencer on top of this first.
# ----------------------------------------------------------------------------------

# a demo of using the Tracker "DSL" API from Python to define compositions
# with somewhat less flexible routing but easier data entry
# SUBJECT TO CHANGE - MASSIVELY

def play():

    # We are building a house of fire, baby.

    song = SongFactory(
        name='Foo',
        author='Your Name'
    )

    song.set(

        Defaults().set(
            bpm = 120,
            scene_bar_count = 8
        ),

        # -- INSTRUMENTS --
        Instruments().set(
            strings = Instrument().set(channel=1),
            lead    = Instrument().set(channel=2),
            # drums   = Instrument().set(channel=3, notation='literal')
        ),

        # -- PATTERNS --
        RandomPatterns(mode='probability').set(
            # chordify_chance_pt = [ 0, 0.5 ]
        ),

        BasicPatterns().set(
            some_jam_pt1 = "4 6 1 6 | 4 4 4 4 | 6 6 4 1 | 1 4 6 4 | 6 4 4 4 | 4 6 4 6",
            some_jam_pt2 = "1 2 3 4 | 3 2 5 1 | 1 1 7 6 | 5 4 3 2 | 1 2 3 4 | 5 6 7 1",
        ),

        RandomPatterns(mode='choice').set(
            # random_pt1 = "1 2 3 4 5 6 7",
            # implies we want a new kind of generator below...
            # velocity_pt1 = [ 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110 ]
        ),

        RandomPatterns(mode='probability').set(
            # chordify_chance_pt1 = [ 0, 0.5, 0.25, 0.125 ]
        ),

        EndlessPatterns().set(
            transpose_pt1 = [ 2, 0, -2 ],
            # duration_pt1 = [ 0.25, 0.25, 0.125, 0.125 ],
            # chordify_pt1 = [ "major", "major", "minor", "major", "pow", "aug"],
            basic_chords = "I IV V I"
        ),

        # --- FX ---
        FxBuses().set(
            arpeggiate_lead = FxBus().set([
                dict(module='arp', splits=[4], octaves='transpose_pt1', mode='locked')
            ]),
        ),

        # -- SCENES --
        Scenes().set(
            # BOOKMARK: FIXME: bar count is not yet implemented as of time of writing, need a camp.band.members.stop or something to implement.  Easy though.
            overture = Scene().set(
                scale = "C4 major",
                bar_count = 12,
                # pre_fx = dict(strings='random_velocity_and_duration'),
                # post_fx = dict(strings='arpeggiate_lead'),
                patterns = dict(strings='basic_chords', lead=[ 'some_jam_pt2', 'some_jam_pt1' ])
            ),
            llama_theme = Scene().set(
                scale = "C4 major",
                bar_count = 12,
                # pre_fx = dict(strings = 'random_velocity_and_duration'),
                # post_fx = dict(strings = 'arpeggiate_strings', lead = 'transpose_lead'),
                post_fx = dict(strings='arpeggiate_lead'),
                patterns = dict(strings = 'basic_chords', lead = [ 'some_jam_pt1', 'some_jam_pt2' ])
            )
        )

    )

    # -- GO! --

    # scene_names = ['overture', 'llama_theme', 'bridge', 'chorus', 'verse', 'chorus', 'verse', 'ending']
    scene_names = ['overture', 'llama_theme' ]
    song.play(scene_names)



if __name__ == "__main__":
    play()
