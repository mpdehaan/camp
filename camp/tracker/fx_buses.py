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

    def __init__(self):
        self._buses = dict()

    def set(self, **buses):

        def callback(song):
            for (bus_name, bus) in buses.items():
                if getattr(bus, '__call__', None) is not None:
                    bus = bus(song)
                if not isinstance(bus, FxBus):
                    raise Exception("only a FxBus is allowed inside of FxBusses set method, got: %s" % bus)
                self._buses[bus_name] = bus
                bus._factory = song
            return self

        return callback

    def as_dict(self):
        return self._buses
