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
    return (a.time)

class Timeline(object):

    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def process_due_events(self, now_time, until_time):
        """
        Processes all events in a loop that will sleep so they are yielded
        at the appropriate time.  Loop runs until "until_time" is reached.
        """

        self.events = sorted(self.events, key=event_sort_key)


        # to avoid timing errors, sleep for N amounts of time but don't use
        # the real clock to know when we are!  Use time instead as an index!

        while now_time <= until_time:

            if len(self.events) == 0:
                sleep_amount = until_time - now_time
                now_time += self._sleep(sleep_amount)
                return
            # get the time the next event should trigger
            last_event_time = self.events[0].time

            if last_event_time <= now_time:
                # the next event needs to trigger now
                event = self.events.pop(0)
                yield event
                continue

            if now_time > until_time:
                return

            # the next event is too far into the future, sleep until
            # the end of the cycle
            if last_event_time >= until_time:
                sleep_amount = until_time - now_time
                now_time = now_time + self._sleep(sleep_amount)
                return

            # the next event isn't ready yet but we can still play
            # it during this cycle
            else:
                sleep_amount = last_event_time - now_time
                now_time = now_time + self._sleep(sleep_amount)
                continue

    def _sleep(self, amount):
        #if amount < 0.05:
        #    return
        #if (amount > 0.02):
            # for trivial sleeps, just fake the sleep and advance the clock.
        time.sleep(amount)
        return amount

    def process_off_events(self):
        """
        Yield all the off events.
        """
        for event in self.events:
            if event.off:
                print(event)
                yield event
