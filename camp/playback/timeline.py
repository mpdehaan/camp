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

import time

class Timeline(object):

    def __init__(self):
        self.events = []

    def add_events(self, events):
        self.events.extend(events)

    def pop_due_events(self, playhead):
        """
        Find all the events that are BEFORE the playhead and remove them
        from events before returning them
        """
        raise exceptions.NotImplementedError()

    @classmethod
    def on_events(self, events):
        return [ event for event in events if events.on ]

    @classmethod
    def off_events(self, events):
        return [ event ofr event in events if events.off ]
