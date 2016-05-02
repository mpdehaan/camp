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

import json

from camp.tracker.defaults import Defaults
from camp.tracker.instruments import Instruments
from camp.tracker.patterns import Patterns, RandomPatterns, BasicPatterns, EndlessPatterns
from camp.tracker.fx_buses import FxBuses
from camp.tracker.fx_bus import FxBus
from camp.tracker.scenes import Scenes
from camp.tracker.scene import Scene
from camp.band.conductor import Conductor
from camp.band.members.performance import Performance

class SongFactory(object):

    __slots__ = [ 'defaults', 'fx_buses', 'scenes', 'instruments', 'patterns' ]

    def __init__(self, name=None, author=None):
        self.defaults = dict()
        # by name, a dict of instrument objects
        self.instruments = dict()
        # by name, a dict of pattern objects
        self.patterns = dict()
        # by name, a  list of instantiated camp.band.member objects
        self.fx_buses = dict()
        # by name, a dict of scene objects
        # scene objects contain chain management code
        self.scenes = dict()

    def pattern(self, name):
        return self.patterns[name]

    def to_data(self):
        """
        Convert the composition to a simple datastructure.
        """

        data = dict(
            defaults = dict(),
            instruments = dict(),
            patterns = dict(),
            fx_buses = dict(),
            scenes = dict()
        )

        for (k, v) in self.instruments.items():
            data['instruments'][k] = v.to_data()

        for (k, v) in self.patterns.items():
            if type(v) == list:
                data['patterns'][k] = v
            else:
                data['patterns'][k] = v.to_data()

        for (k, v) in self.fx_buses.items():
            data['fx_buses'][k] = v.to_data()

        for (k,v) in self.scenes.items():
            data['scenes'][k] = v.to_data()
        return data

    def to_json(self):
        """
        Convert the composition to JSON
        """
        data = self.to_data()
        return json.dumps(data, indent=4)

    def save(self, filename):
        """
        Save the composition to disk.
        """
        fh = open(filename, "w")
        fh.write(self.to_json())
        fh.close()

    def set_defaults(self, **data):
        """
        Configures/reconfigures a series of global settings using kwargs.  Some of these values may later be overriden at the scene
        or other level.
        """
        assert type(data) == dict
        # example:
        # song.set_defaults(bpm=120)
        # (each of these set_* methods temporarily creates a validation object but the internal storage is a dictionary in SongFactory)
        self.defaults.update(Defaults(self, **data).as_dict())

    def set_fx_buses(self, **data):
        """
        Defines one or more FxBus objects using kwargs.  Each value should be a FxBus object, which in turn is constructed by a list of 1 or more
        module specifications that correspond to camp.band.member objects.
        """
        # example
        # song.set_fx_busses(
        #   arpeggiate_lead = FxBus(
        #      [module='arp', params=dict(splits=[4], octaves='transpose_pt1', mode='locked')])
        # )
        self.fx_buses.update(FxBuses(self, **data).as_dict())

    def set_instruments(self, **data):
        """
        Defines/redefines one or more instruments using kwargs.  Each value is an Instrument object.
        """
        assert type(data) == dict
        # example
        # song.set_instruments(
        #    strings = Instrument().set(channel=1),
        #    lead    = Instrument().set(channel=2),
        #)
        self.instruments.update(Instruments(self, **data).as_dict())

    def set_scenes(self, **data):
        """
        Defines/redefines one or more scenes using kwargs.  Each value is a Scene object.
        """
        assert type(data) == dict
        # example
        # song.set_scenes(
        #    overture = Scene(
        #        scale = "C4 major",
        #        bar_count = 12,
        #        # pre_fx = dict(strings='random_velocity_and_duration'),
        #        # post_fx = dict(strings='arpeggiate_lead'),
        #        patterns = dict(strings='basic_chords', lead=[ 'some_jam_pt2', 'some_jam_pt1' ])
        #    ),
        #    llama_theme = Scene(
        #        scale = "C4 major",
        #        bar_count = 12,
        #        # pre_fx = dict(strings = 'random_velocity_and_duration'),
        #        # post_fx = dict(strings = 'arpeggiate_strings', lead = 'transpose_lead'),
        #        post_fx = dict(strings='arpeggiate_lead'),
        #        patterns = dict(strings='basic_chords', lead=[ 'some_jam_pt1', 'some_jam_pt2' ])
        #    )
        #)
        self.scenes.update(Scenes(self, **data).as_dict())

    def set_patterns(self, typ='basic', mode=None, patterns=None):
        """
        Defines one or more patterns using kwargs.  Can specify endless or random patterns by changing 'typ'.
        Each typ may also respond to submodifier 'mode'.
        """
        assert type(patterns) == dict
        #Example:
        # song.set_patterns(typ='random', patterns=dict(
        #    scale  =[1,2,3,4,5,6,7],
        #    melody ="1 4 2 3 4 1",
        #    chords ="I IV V I"
        #))

        which = None
        if typ == 'basic':
            which = BasicPatterns
        elif typ == 'random':
            which = RandomPatterns
        elif typ == 'endless':
            which = EndlessPatterns
        else:
            raise Exception("unknown pattern type: %s" % typ)
        self.patterns.update(which(self, patterns=patterns).as_dict())


    def handle_scene(self, scene_name, play=False):

        scene = self.scenes.get(scene_name)
        if scene is None:
            raise Exception("no such scene: %s" % scene_name)
        conductor = Conductor(signal=scene.get_signals(), performance=scene.get_output())
        if play:
            conductor.start()

    def play(self, scene_names):

        # first validate
        for scene_name in scene_names:
            self.handle_scene(scene_name, play=False)

        # then play
        for scene_name in scene_names:
            self.handle_scene(scene_name, play=True)
