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

from camp.utils import instance_produce, exclude_dict
from camp.band.selectors.endlessly import Endlessly

# FxBus([
#     dict(module='velocity', levels='velocity_pt1'),
#    dict(module='duration', levels='duration_pt1')
# ]),

class FxBus(object):

    def __init__(self, member_list):
        self._nodes = [ member.copy() for member in member_list ]

    def nodes(self):
        return [ node.copy() for node in self._nodes ]

    def to_data(self):
        return [ x.to_data() for x in self._nodes ]
