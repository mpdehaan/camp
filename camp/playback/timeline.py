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

def event_sort_key(a):
    return (0 - a.time)
    
class Timeline(object):

    def __init__(self):
        self.events = []

    def add_event(self, event, now_time):
        if now_time is None or now_time is 0:
            raise Exception("TIME ERROR!")
        event.time = now_time
        self.events.append(event)

    def process_due_events(self, until_time):
        """
        Processes all events in a loop that will sleep so they are yielded
        at the appropriate time.  Loop runs until "until_time" is reached.
        """

        self.events.sort(key=event_sort_key)
        now_time = time.time()
        while now_time <= until_time:
            now_time = time.time()
            if len(self.events) == 0:
                return
            # get the time the next event should trigger
            last_event_time = self.events[-1].time
            # if this time is BEFORE or EQUAL to now, fire it off
            if last_event_time <= now_time:
                # the next event needs to trigger now
                print(self.events[-1])
                yield self.events[-1]
                self.events.pop()
                continue
            elif last_event_time <= until_time:
                # the event has not occured yet but there is time to wait
                sleep_amount = last_event_time - now_time
                print("sleep %s" % sleep_amount)
                time.sleep(sleep_amount)
                continue
            else:
                # the calculation code will need to fire, all events
                # are in the future beyond the next appointed calculation
                # time.  As such, sleep until then, but do not longer
                sleep_amount = until_time - now_time
                print("sleep %s" % sleep_amount)
                time.sleep(sleep_amount)
                return

    def process_off_events(self):
        """
        Yield all the off events.
        """
        for event in self.events:
            if event.off:
                print(event)
                yield event
