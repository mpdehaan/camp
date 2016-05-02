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

from camp.tracker.fx_bus import FxBus

class FxBuses(object):

    __slots__ = [ '_buses', '_factory' ]

    def __init__(self, song, **buses):

        self._factory = song
        self._buses = dict()

        for (bus_name, bus) in buses.items():
            if getattr(bus, '__call__', None) is not None:
                bus = bus(song)
            if not isinstance(bus, FxBus):
                raise Exception("only a FxBus is allowed inside of FxBusses set method, got: %s" % bus)
            self._buses[bus_name] = bus
            bus._factory = song

    def as_dict(self):
        return self._buses

    def to_data(self):
        result = dict(cls='camp.tracker.fx_bus.FxBuses')
        for (k,v) in self._buses:
            result['data'][k] = v.to_data()
        return result
