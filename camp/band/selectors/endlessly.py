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

from camp.band.selectors.selector import Selector

def endlessly_generate(alist):
    while True:
        for item in alist:
            yield item

class Endlessly(Selector):

    def __init__(self, alist, mode=None):
        self.data = alist
        self.my_generator = endlessly_generate(alist)

    def draw(self):
        result = next(self.my_generator)
        return result

    def to_data(self):
        return dict(cls="camp.band.selectors.selector.Endlessly", data=dict(alist=self.data))
