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

from camp.tracker.instrument import Instrument

class Instruments(object):

    __slots__ = [ "_instruments", "_factory" ]

    def __init__(self, song, **instruments):

        self._factory = song
        self._instruments = dict()

        for (instrument_name, instrument) in instruments.items():

            print("CREATING INSTRUMENT: %s" % instrument)

            instrument._factory = song
            
            print(instrument.channel)
            if instrument.channel is None:
                raise Exception("DEBUG: channel is None")


            if type(instrument) != Instrument:
                raise Exception("instruments collection requires an instrument")

            print("AIGHT")
            self._instruments[instrument_name] = instrument

    def as_dict(self):
        return self._instruments

    def to_data(self):
        results = dict(cls="camp.tracker.instruments.Instruments")
        for (k,v) in self._instruments():
            results['data'][k] = v.to_data()
