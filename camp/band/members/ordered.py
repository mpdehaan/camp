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

from camp.band.members.member import Member

class Ordered(Member):

    # see examples/13_ordering.py

    def __init__(self, channel=None, sources=None):

        # TODO: later also support step transpositions
        # or even grabbing the next note in the scale

        super().__init__(channel=channel)

        assert sources is not None
        self._sources = sources
        self.reset()

    def reset(self):
        self.sources_looper = self.draw_from(self._sources)
        self.current_source = next(self.sources_looper)
        self.current_source.reset()

    def _get_events_from_a_source(self, event, start_time, end_time):

        while True:
            print("CURRENT SOURCE: %s" % self.current_source)
            events = self.current_source.signal(event, start_time, end_time)
            if len(events) != 0:
                return [ event.copy() for event in events ]
            try:
                self.current_source = next(self.sources_looper)
                self.current_source.reset()
            except StopIteration:
                return []


    def on_signal(self, event, start_time, end_time):

        event = event.copy()
        events = self._get_events_from_a_source(event, start_time, end_time)

        for event in events:
            print("--")
            for send in self.sends:
                print("SIGNAL SEND TO: %s" % send)
                send.signal(event, start_time, end_time)

        return events
