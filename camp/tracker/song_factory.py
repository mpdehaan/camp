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

    def set(self, *items):

        for item in items:
            if hasattr(item, '__call__'):
                item = item(self)
            item._factory = self
            if isinstance(item, Defaults):
                which = self.defaults
            elif isinstance(item, FxBuses):
                which = self.fx_buses
            elif isinstance(item, Instruments):
                which = self.instruments
            elif isinstance(item, Scenes):
                which = self.scenes
            elif isinstance(item, Patterns):
                which = self.patterns
            else:
                raise Exception("unknown object type: %s" % item)
            which.update(item.as_dict())

    def handle_scene(self, scene_name, play=False):

        scene = self.scenes.get(scene_name)
        if scene is None:
            raise Exception("no such scene: %s" % scene_name)
        conductor = Conductor(signal=scene.get_signals(), output=scene.get_output())
        if play:
            conductor.play()

    def play(self, scene_names):

        # first validate
        for scene_name in scene_names:
            self.handle_scene(scene_name, play=False)

        # then play
        for scene_name in scene_names:
            self.handle_scene(scene_name, play=True)
