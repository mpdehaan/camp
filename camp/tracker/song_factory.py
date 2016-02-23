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

OBSOLETE = """

    def from_data(self, data):

        self._check_dict('tracker', data)
        self._check_required_keys('tracker', data)

        self.set_metadata(data.get('metadata'), dict())
        self.set_defaults(data.get('defaults'), dict())
        self.set_patterns(data['patterns'])
        self.set_instruments(data.get('instruments', dict())
        self.set_fx_busses(data.get('fx_busses'), dict())
        self.set_scenes(data['scenes'])
        self.set_scene_order(data['scene_order'])

        self._configure_scene_instruments()

    def _check_list(self, name, alist):
        if type(alist) != list:
            raise Exception("expecting '%s' to be a list" % name)

    def _check_dict(self, name, adict):
        if type(alist) != list:
            raise Exception("expecting '%s' to be a list" % name)

    def _check_valid_keys(self, name, keys):
        valid_list = VALID_KEYS[name].split()
        invalid = []
        for k in keys:
            if k not in valid_list:
                invalid.append(k)
        if len(invalid) > 0:
            raise Exception("invalid key(s) given to %s: %s" % (name, invalid))

    def _check_required_keys(self, name, keys, required_list):
        required_list = REQUIRED_KEYS[name]
        if required_list is None:
            return
        required_list = required_list.split()
        missing = []
        for k in required_list:
            if k not in keys:
                missing.append(k)
        if len(missing) > 0:
            raise Exception("missing key(s) in %s: %s" % (name, missing))




    def set_defaults(self, data):

        self._check_valid_keys('defaults', data.keys(), VALID_DEFAULT_KEYS)
        self.defaults = data

    def set_instruments(self, data):

        self._check_dict('instruments', data)
        for (k, instrument_defition) in data.iteritems():
            self._check_valid_keys('instrument', v), VALID_INSTRUMENT_KEYS)
            notation = data.get('notation', roman)
            flags = self._exclude_dict(data, ['notation'])
            empty_notation_instance = self._factory_produce('camp.band.members', notation, flags)
            self.instruments[k] = empty_notation_instance
        if len(self.instruments.keys()) == 0:
            raise Exception("no instruments assigned!")

    def _listify(self, msg, data):
        if instanceof(data, str):
            return = data.replace("|","").split()
        elif type(data) == list:
            return data
        else:
            raise Exception("expecting list for %s" % msg)

    def _exclude_keys(self, data, exclude=None):
        results = dict()
        for (k,v) in data:
            if k not in exclude:
                results[k] = v
        return results

    def _build_pattern(self, name=None, spec=None, assignment=None):
        alist = self._listify("pattern '%s'" % name, assignment)


        select_type = pattern_spec.get('select', None)
        flags = self._exclude_keys(pattern_spec, ['select'])

        # FIXME: instantiate class by name in camp.band.selectors namespace
        if select_type is None or select_type = 'once':
            return alist
        else:
            return self._factory_produce('camp.band.selectors.%s', select_type.title, flags)

    def set_patterns(self, data):
        # see demo_tracks/exploring.yml for usage
        self._check_list('patterns', data)
        for pattern_spec in data:

            self._check_list('pattern_block', pattern_spec)
            self._check_required_keys('pattern_block', pattern_spec)


            for (variable, assignment) in pattern_spec['assign']:
                self.patterns[variable] = self._build_pattern(name=variable, spec=pattern_spec, assignment=assignment)

    def _build_fx_bus(self, name=None, data=None):

        self._check_list('fx_bus', data)

        root_fx = None
        last_fx = None
        should_stitch = None

        if len(data) <= 0:
            raise Exception("empty fx_bus: %s" % name)

        for node in data:

            self._check_required_keys('fx_bus_spec', node)

            should_stitch = False
            if last_fx is not None:
                should_stitch = True

            module = node.get('module')
            flags = self._exclude_dict(node, 'module')
            result = self.factory_produce('camp.band.musicians', module, **flags)

            if root_fx is None:
                root_fx = result
            if should_stitch:
                result.send_to(last_fx)
            last_fx = result

        self.fx_chain_heads[name] = root_fx
        self.fx_chains_tails[name] = last_fx


    def set_fx_busses(self, data):

        self._check_dict('fx_busses', data)


        for (name, fx_bus) in data:
            should_stitch = False
            if last_fx is not None:
                should_stitch = True

            result = self.fx_busses[name] = self._build_fx_bus(name=name, fx_bus=fx_bus)
            if root_fx is None:
                root_fx = result
            if should_stitch:
                result.send_to(last_fx)
            last_fx = result

    def _check_instrument(self, name):
        if name not in self.instruments:
            raise Exception("unknown instrument: %s" % name)

    def _check_pattern(self, name):
        if name not in self.patterns:
            raise Exception("unknown pattern: %s" % name)

    def _check_fx_bus(self, name):
        if name not in self.fx_chain_heads:
            raise Exception("unknown fx bus: %s" % name)
        if name not in self.fx_chain_tails:
            raise Exception("mal-formed fx bus: %s" % name)

    def _check_fx_assigments(self, instrument_name, fx_assignments):
        self._check_instrument(instrument_name)
        assignments = self._listify('fx_assignment', fx_assignments)
        self._check_list('fx_assignment', fx_assignments)
        for fx_bus in fx_assignments:
            if fx_bus not in self.fx_chain_heads:
                raise Exception("unknown fx chain: %s" % fx_bus)
        return assignments

    def _check_pattern_assignments(self, instrument_name, pattern_assignment):
        self._check_instrument(instrument_name)
        assignments = self._listify('pattern_assignment', pattern_assignment)
        for pattern_name in assignments:
            self._check_pattern(pattern_name)
        return assignments

    def set_scenes(self, data):

        self._check_dict('scenes', data)

        for (scene_name, scene_data) in data.iteritems():

            self._check_dict('scene', scene)
            self._check_valid_keys('scene', scene)
            self._check_required_keys('scene', scene)

            for (param_name, param_value) in scene.iteritems():


                if param_name in [ 'pre_fx', 'post_fx' ]:

                    self._check_dict('fx_assignment', param_value)
                    for (instrument_name, fx_assignments) in param_value.iteritems():
                        assignments = self._check_fx_assignments(instrument_name, fx_assignments)

                        composite_key = "%s/%s" % (scene_name, instrument_name)
                        if param_name == 'pre_fx':
                            self.pre_fx[composite_key] = assignments
                        elif param_name == 'post_fx':
                            self.post_fx[composite_key] = assignments


                if param_name in 'patterns':

                    self._check_dict('pattern_assignment', param_value)

                    for (instrument_name, pattern_assignment) in param_value.iteritems():
                        assignments = self._check_pattern_assignments(instrument_name, pattern_assignment)

                        composite_key = "%s/%s" % (scene_name, instrument_name)
                        self.pattern_assignments[composite_key] = assignments

    def _check_scene(name):
        if 'name' not in self.scenes:
            raise Exception("reference to missing scene: %s" % name)

    def set_scene_order(self, data):
        self._check_list('song', data)
        for scene_name in data:
            self._check_scene(scene_name)

    def _get_scene_instruments(self, output)

        heads = []
        tails = []

        for scene_name in self.scenes.keys():


            bpm = 'FIXME'
            stop_seconds = 'FIXME'
            scale = 'FIXME'


            for (instrument_name, reader_instance) in self.instruments:

                # in support of future things playing differnent scales or whatever I guess.
                scale_choices = Endlessly(scale)
                source = ScaleSource(scales=scale_choices)
                heads.append(source)

                composite_key = "%s/%s" % (scene_name, instrument_name)

                my_sources = []

                for p in self.patterns[composite_key]:
                    reader = self.instruments[instrument_name].copy()
                    reader.symbols = p
                    my_sources.append(reader)

                ordered = Ordered(sources=my_sources)
                reader = self.instruments.copy()

                # if an PRE FX chain is specified, connect to the foot of the FX chain

                my_pre_fx = self.pre_fx.get(composite_key, None)
                if my_pre_fx is not None:
                    fx_chain_tails[my_pre_fx].send_to(ordered)

                # if a POST FX chain is specified, connect that to the foot
                my_post_fx = self.post_fx.get(composite_key, None)
                if my_post_fx is not None:
                    ordered.send_to(fx_chain_heads[my_post_fx])
                    tail = fx_chain_tails[my_post_fx]
                    tails.append(tail)
                else:
                    tails.append(ordered)


    def play()

        # first validate everything
        for scene in self.scene_order:
            (heads, tails) = self._get_scene_instruments(self)

        for scene in self.scene_order:
            (heads, tails) = self._get_scene_instruments(self)
            output = Performance(bpm=120, stop_seconds=10) # FIXME
            output.listens_to(tails)
            conductor = Conductor(signals=heads, output=output)
            conductor.play()

"""
