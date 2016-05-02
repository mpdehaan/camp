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

from camp.band.members.scale_source import ScaleSource
from camp.band.members.performance import Performance
from camp.core.scale import scale as core_scale

VALID_NOTATIONS = [ 'roman', 'literal' ]

class Instrument(object):

    def __init__(self, channel=None, notation='roman'):

        self.channel = channel
        self.notation = notation

        if type(self.channel) != int:
            raise Exception("channel must be set, as an integer, got: %s" % self.channel)
        if notation not in VALID_NOTATIONS:
            raise Exception("invalid notation type: %s" % notation)

    def to_data(self):
        return dict(cls="camp.band.tracker.instrument.Instrument", data=dict(channel=self.channel, notation=self.notation))
