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

import copy

class Event(object):

    def __init__(self, time=None, channel=None, notes=None, velocity=None, off=False, duration=None, flags=None, keep_alive=False):

        if channel is not None:
            assert type(channel) == int

        if velocity is not None:
            assert type(velocity) == int

        if flags is not None:
            assert type(flags) == dict
            self.flags = flags
        else:
            self.flags = dict()

        self.keep_alive = keep_alive
        self.time = time
        self.channel = channel
        self.notes = notes
        self.velocity = velocity
        self.duration = duration
        self.off = off

    def add_flags(self, **kwargs):
        for (k,v) in kwargs.items():
            self.flags[k]=v

    def copy(self):
        notes = None
        if self.notes:
            notes = [ n.copy() for n in self.notes ]
        flags = copy.deepcopy(self.flags)
        return Event(
            time=self.time,
            channel=self.channel,
            notes=notes,
            velocity=self.velocity,
            duration=self.duration,
            flags=flags,
            off=self.off,
            keep_alive=self.keep_alive)

    def __repr__(self):
        on = "ON"
        if self.off:
            on = "OFF"
        return "<Event %s (time=%s,channel=%s,notes=%s,velocity=%s,duration=%s,flags=%s,keep_alive=%s)>" % \
            (on, self.time, self.channel, self.notes, self.velocity, self.duration, self.flags, self.keep_alive)
