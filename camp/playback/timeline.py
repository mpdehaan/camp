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
from collections import namedtuple




class Timeline(object):

    def __init__(self):
        self.events = []

    def add_event(self, event, now_time):
        if now_time is None or now_time is 0:
            raise Exception("TIME ERROR!")
        event.time = now_time
        self.events.append(event)

    def pop_due_events(self, now_time):
        """
        Find all the events that are BEFORE the playhead and remove them
        from events before returning them
        """
        print("timeline:: now is :: %s" % now_time)
        to_return = [ event for event in self.events if self._is_due(event, now_time) ]
        to_keep = [ event for event in self.events if not self._is_due(event, now_time) ]
        self.events = to_keep
        print("timeline :: remaining events :: %s" % to_keep)
        print("timeline :: play events :: %s" % to_return)
        return to_return

    def _is_due(self, event, now_time):
        return event.time <= now_time

    def on_events(self):
        return [ event for event in self.events if event.velocity not in [ 0, None ] ]

    def off_events(self):
        return [ event for event in self.events if event.velocity in [ 0, None ] ]
