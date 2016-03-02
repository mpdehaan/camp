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

from camp.band.members.scale_source import ScaleSource
from camp.band.members.performance import Performance
from camp.band.members.roman import Roman
from camp.band.members.literal import Literal
from camp.band.members.ordered import Ordered
from camp.core.scale import scale as core_scale

class Scene(object):

    def __init__(self):
        pass

    def set(self, bpm=None, scale=None, pre_fx=None, post_fx=None, patterns=None, bar_count=None):

        def callback(song):

            self._factory = song
            self.scale = scale
            self.bpm = None
            self.pre_fx = pre_fx
            self.post_fx = post_fx
            self.patterns = patterns
            self.bar_count = bar_count

            self._factory = None # set up by scenes.py
            self._scale_source = ScaleSource(scales=core_scale(self.scale))
            self._output = None
            self._players = dict()

            return self

        return callback

    def build(self):

        self._build_output()
        self._build_fx_chains()
        self._build_players()
        self._build_interconnects()

    def _build_output(self):

        # FIXME: the system uses stop_seconds to cap a scene at a given number of seconds
        # but we are really more interested in beats.  We probably want to attach a new timer
        # instance to the output to make this work instead, until then stop_seconds is hard coded
        # for DEBUG only and should be removed.  This should use defaults/scene_max_bars and bars on
        # the scene object.

        if self.bpm is None:
            self.bpm = self._factory.defaults['bpm']
        self._output = Performance(bpm=self.bpm, stop_seconds = 10)

    def _build_fx_chains(self):
        for (chain_name, bus) in self._factory.fx_buses.items():
            previous = None
            nodes = bus.nodes()
            for item in nodes:
                if previous is not None:
                    previous.sends = []
                    previous.send_to(item)
                previous = item

    def _build_players(self):

        for (instrument_name, pattern_list) in self.patterns.items():

            instrument = self._factory.instruments[instrument_name]
            channel = instrument.channel
            notation = instrument.notation
            sources = []

            for pattern_name in pattern_list:

                pattern = self._factory.patterns.get(pattern_name, None)

                real_pattern = None

                if notation == 'roman':
                    real_pattern = Roman(symbols=pattern)
                elif notation == 'literal':
                    real_pattern = Literal(symbols=pattern)
                else:
                    raise Exception("unknown notation type for instrument: %s" % instrument_name)

                sources.append(real_pattern)

            self._players[instrument_name] = Ordered(sources=sources)

    def _stitch_fx_chain(self, assignments, instrument_name, from_node, to_node):

        print("ASSIGNMENTS: %s" % assignments)
        print("FX BUSES: %s" % self._factory.fx_buses)

        fx_chain_name = assignments[instrument_name]
        if fx_chain_name not in self._factory.fx_buses:
            # FIXME: typed exceptions everywhere to make it easier for higher level apps
            raise Exception("fx bus not found: %s" % fx_chain_name)
        fx_chain = self._factory.fx_buses[fx_chain_name].nodes()
        head = fx_chain[0]
        tail = fx_chain[-1]
        from_node.send_to(head)
        tail.send_to(to_node)

    def _build_interconnects(self):

        for (instrument_name, player) in self._players.items():

            player = self._players[instrument_name]

            # TODO: consider whether it makes sense for a FxBus to connect to another FxBus
            # ignoring for now.

            if instrument_name not in self.pre_fx:
                # connect directly to source
                self._scale_source.send_to(self._players[instrument_name])
            else:
                # ensure prefx is coupled to source and tail is coupled to output
                self._stitch_fx_chain(self.pre_fx, instrument_name, self._scale_source, player)


            if instrument_name not in self.post_fx:
                # connect directly to output
                player.send_to(self._output)
            else:
                # ensure player is coupled to head of post fx and tail is coupled to output
                self._stitch_fx_chain(self.post_fx, instrument_name, player, self._output)

    def get_signals(self):
        return [ self._scale_source ]

    def get_output(self):
        return [ self._output ]
