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

import random
import copy

def endlessly_generate(alist, mode):

    alist = copy.copy(alist)

    while True:

        if mode == 'choice':

            print("HIT!")
            choice = random.choice(alist)

            if type(choice) == dict and 'value' in choice:
                value = choice.get('value', None)
                length = choice.get('hold', 1)
                if value is None:
                    raise Exception("expecting value in choice expression, usage of Randomly is munged")
                for count in range(0, length):
                    yield value
            else:
                yield choice

        elif mode == 'probability':

            for item in alist:

                zero_to_one = random.random()
                print("V,I = %s, %s" % (zero_to_one, item))

                if zero_to_one > item:
                    yield False
                else:
                    yield True

        elif mode == 'exhaust':

            my_list = alist[:]
            while len(my_list) > 0:
                print("DRAWING")
                length = len(my_list)
                index = random.randint(0,length) - 1
                item = my_list.pop(index)
                print("EXHAUST YIELDS: %s" % item)
                yield item
            print("ALL DONE")

        elif mode == 'human':

            while True:

                length = len(alist)
                index = random.randint(0,alist) - 1
                item = alist.pop(index)
                yield item

        else:

            raise Exception("unknown Randomly mode: %s" % mode)


class Randomly(Selector):

    # see examples/11_randomness.py for usage

    # TODO: implement serialism by allowing a serialism=True flag which will pop
    # the item off the list once consumed.  When done, update comments in 11_randomness.py
    # to show the example.

    def __init__(self, alist, mode='choice'):
        self.data = alist
        self.mode = mode
        self.my_generator = endlessly_generate(alist, mode)

        random.seed()


    def draw(self):
        result = next(self.my_generator)
        return result

    def to_data(self):
        return dict(cls="camp.band.selectors.selector.Randomly", data=dict(alist=self.data, mode=self.mode))
