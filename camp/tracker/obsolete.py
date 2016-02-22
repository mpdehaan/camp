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

VALID_KEYS = dict(
    defaults = "bpm max_bars_per_scene"
    instrument = "channel notation"
    scene = "scale max_bars pre_fx post_fx patterns"
    tracker = "scenes scene_order instruments patterns metadata fx_busses"
)

REQUIRED_KEYS = dict(
    defaults = None
    instrument = "channel"
    pattern_block = "assign"
    fx_bus_spec = "module"
    scene = "scale patterns"
    tracker = "scenes scene_order instruments patterns"
)

# TODO: this is rough yet - want to do lots of refactoring, split into data objects that do individual validation
# this is just pass one to get something working and not the final version

# TODO: implement factory_produce method.

# TODO: find and remove dead code

# TODO: ensure various flags like max_bars_per_scene, bpm, etc, everywhere all do something

# TODO: wrap various assignments so there is more debug while things are rolling

VALID_PATTERN_TYPES = [ 'endlessly', 'repeatedly', 'randomly', 'once' ]

from camp.band.selectors.repeatedly import Repeatedly
from camp.band.selectors.endlessly import Endlessly
from camp.band.selectors.randomly import Randomly

class SongFactory(self)

    def __init__(self):

        # a bunch of defaults
        #self.defaults = dict()

        # a raw dictionary
        #self.metadata = dict()

        # a dict of name -> Roman() or Literal() instances, with symbols array unassigned
        #self.instruments = dict()

        # a list of selectors by name, or flat arrays, i.e. [] or Endlessly() or Randomly() or Repeatedly()
        #self.patterns = dict()

        # a list of references to the head node of a FX chain by composite key (scene_name/instrument_name)
        #self.post_fx = dict()

        # a list of references to the foot note of a FX chain by composite key (scene_name/instrument_name)
        #self.pre_fx = dict()

        # mostly unfiltered scene data by name, including params like 'bpm', etc
        #self.scenes = dict()

        # a list of scene names in order to play them, which may repeat.
        #self.scene_order = []

        #self.fx_chain_heads = dict()
        #self.fx_chain_tails = dict()

        # conductor objects by scene name, with fully populated objects - this happens after the initial
        # data load step and right before playback starts
        #self.conductors = []

        # fully built instrument chains for each scene, using the scene/instrument composite key
        #self.scene_instruments = dict()

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


    def set_metadata(self, data):
        """
        metadata = dict(
            name = "This Song",
            author = "Your Name",
            email = "you@example.com",
            date = "1/1/2016",
        )
        """

        # not used presently
        self.metadata = data

    def set_defaults(self, data):

        self._check_valid_keys('defaults', data.keys(), VALID_DEFAULT_KEYS)
        self.defaults = data

    def set_instruments(self, data):
        """
        instruments = dict(
            strings = dict(channel=1),
            lead    = dict(channel=2),
            drums   = dict(channel=3, notation='literal')
        ),
        """
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
        """
        fx_busses = dict(
                arpeggiate_strings = "FIXME",
                random_velocity_and_duration = [
                    dict(module='velocity', levels='velocity_pat'),
                    dict(module='duration', levels='duration_pat')
                ],
                chordify_lead = [
                    dict(module='chordify', types='chordify_pat', when='chordify_chance_pat')
                ],
                transpose_lead = [
                    dict(module='transpose_lead', octaves='transpose_pat')
                ]
            )
        """
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
