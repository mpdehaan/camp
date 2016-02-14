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

    def add_event(self, event):
        assert event.time is not None and event.time != 0
        self.events.append(event)

    def process_due_events(self, until_time):
        """
        Processes all events in a loop that will sleep so they are yielded
        at the appropriate time.  Loop runs until "until_time" is reached.
        """

        self.events = sorted(self.events, key=event_sort_key)

        #print("********")
        #print("EVENTS")
        #for x in self.events:
        #    print(x)
        #print("********")

        now_time = time.time()
        while now_time <= until_time:

            print("NOW %s vs UNTIL %s" % (now_time, until_time))

            now_time = time.time()
            if len(self.events) == 0:
                sleep_amount = until_time - now_time
                self._sleep(sleep_amount)
                return
            # get the time the next event should trigger
            last_event_time = self.events[-1].time

            if last_event_time <= now_time:
                # the next event needs to trigger now
                print(self.events[-1])
                yield self.events[-1]
                self.events.pop()
                continue
            else:
                # the next event is LATER than now
                if last_event_time > until_time:
                    print("M1")
                    sleep_amount = until_time - now_time
                else:
                    print("M2")
                    sleep_amount =  last_event_time - now_time
                self._sleep(sleep_amount)
                continue

        raise Exception("LOOP EXIT!")

    def _sleep(self, amount):
        #if amount < 0.05:
        #    return
        time.sleep(amount)

    def process_off_events(self):
        """
        Yield all the off events.
        """
        for event in self.events:
            if event.off:
                print(event)
                yield event
