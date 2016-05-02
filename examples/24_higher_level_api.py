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
from camp.band.members.chordify import Chordify
from camp.band.members.arp import Arp

# ---------------------------------------------------------------------------------
# WARNING -- THIS EXAMPLE IS UNDER DEVELOPMENT CURRENTLY
# AND IS NOT FINAL.  What this shows is how to describe a composition more
# conceptually.  The sequencer (interface for people who do not want to write code)
# will build off of this.
# ----------------------------------------------------------------------------------


def play():

    # We are building a house of fire, baby.

    song = SongFactory(
        name='Foo',
        author='Your Name'
    )

    song.set_defaults(
        bpm = 120,
        scene_bar_count = 8
    )

    song.set_instruments(
        strings = Instrument(channel=1),
        lead    = Instrument(channel=1),
    )

    song.set_patterns(typ='basic', patterns=dict(
        some_jam_pt1 = "4 6 1 6 | 4 4 4 4 | 6 6 4 1 | 1 4 6 4 | 6 4 4 4 | 4 6 4 6",
        some_jam_pt2 = "1 2 3 4 | 3 2 5 1 | 1 1 7 6 | 5 4 3 2 | 1 2 3 4 | 5 6 7 1",
    ))

    song.set_patterns(typ='random', mode='probability', patterns=dict(
        # chordify_chance_pt = [ 0, 0.5 ]
    ))

    song.set_patterns(typ='random', mode='exhaust', patterns=dict(
        serialism = "1 2 3 4 5 6 7 8 9 10 11 12"
    ))

    song.set_patterns(typ='random', mode='choice', patterns=dict(
        # random_pt1 = "1 2 3 4 5 6 7",
        # implies we want a new kind of generator below...
        # velocity_pt1 = [ 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110 ]

    ))

    song.set_patterns(typ='random', mode='probability', patterns=dict(
        # chordify_chance_pt1 = [ 0, 0.5, 0.25, 0.125 ]
    ))

    song.set_patterns(typ='endless', patterns=dict(
        chord_sequence = [ 'major', 'minor', 'power' ],
        subdivide_arp = [ 3 ],
        transpose_pt1 = [ 2, 0, -2 ],
        # duration_pt1 = [ 0.25, 0.25, 0.125, 0.125 ],
        # chordify_pt1 = [ "major", "major", "minor", "major", "pow", "aug"],
        basic_chords = "I IV V I",
        boring_part = "1",
        transpose_arp = [ 0, 4, 5 ]
    ))

    # --- FX ---
    song.set_fx_buses(
        chordify_lead = FxBus([
            Chordify(types=song.pattern('chord_sequence'))
        ]),
        arpeggiate_lead = FxBus([
             Arp(semitones=song.pattern('transpose_arp'), splits=song.pattern('subdivide_arp'), octaves=song.pattern('transpose_pt1'), mode='locked')
        ])
    )

    song.set_scenes(
        # BOOKMARK: FIXME: bar count is not yet implemented as of time of writing, need a camp.band.members.stop or something to implement.  Easy though.
        overture = Scene(
            scale = "C4 chromatic",
            bar_count = 12,
            # pre_fx = dict(strings='random_velocity_and_duration'),
            post_fx = dict(strings='chordify_lead'),
            patterns = dict(strings='serialism')
        ),
        llama_theme = Scene(
            scale = "C5 minor",
            bar_count = 12,
            # pre_fx = dict(strings = 'random_velocity_and_duration'),
            # post_fx = dict(strings = 'arpeggiate_strings', lead = 'transpose_lead'),
            post_fx = dict(strings='arpeggiate_lead'),
            patterns = dict(strings='boring_part', lead=[ 'some_jam_pt1', 'some_jam_pt2' ])
        )
    )

    # -- GO! --

    # scene_names = ['overture', 'llama_theme', 'bridge', 'chorus', 'verse', 'chorus', 'verse', 'ending']
    scene_names = ['overture', 'llama_theme' ]

    #song.play(scene_names)

    print(song.to_json())


if __name__ == "__main__":
    play()
