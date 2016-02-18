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

class Member(object):

    """
    camp.band.member Member is the base class for all band member plugins.
    Each implements on_signal below.
    """

    def __init__(self, channel=None, when=True):
        """
        Not every band member must specify a MIDI channel, but along each
        line in the chain it should be specified somewhere.
        """
        self.sends = []
        self.channel = channel
        self._when = when

        # FIXME: BUGLET?  Depends how you use it.
        # currently reset does NOT reset the draw_from on the when.
        # to do this, we'll need to make sure every reset() calls super()
        # as it should.  That's minor though.
        self.when = self.draw_from(self._when)

    def reset(self):
        """
        Restarts all iterators over from the beginning.
        """
        raise NotImplementedError()

    def draw_from(self, item):
        """
        In various places a band member needs to draw from a list.
        The default form of drawing from an array is to pop off the first
        element and consume it.  However, when Selectors are employed, we might
        loop endlessly over the selection.  This method exists to hide
        the need to understand choosers from those either building a band member
        or using the API at the simplest level.
        """
        if item is None:
            # this allows optional generators to be turned off.
            while True:
                yield None
        elif type(item) == list:
            for x in item:
                yield x
        elif isinstance(item, Selector):
            while True:
                try:
                    yield item.draw()
                except StopIteration:
                    return
        else:
            while True:
                yield item

    def send_to(self, obj):
        """
        Indicates what band members this band member informs.
        This can be thought as the opposite of listens_to.
        """
        if type(obj) == list:
            for x in obj:
                self.sends.append(x)
        else:
            self.sends.append(obj)
        return obj

    def listens_to(self, obj):
        """
        An alternate way of recording a communication arrangement
        that is a bit more natural.
        """
        if type(obj) == list:
            for x in obj:
                x.sends.append(self)
        else:
            obj.sends.append(self)
        return self

    def chain(self, chain_list):
        """
        A quick way of setting up a lot of nodes to output into one another.
        Returns the head and tail of the chain.
        See tests/band.py.
        """


        assert type(chain_list) == list
        assert len(chain_list) > 0

        item = chain_list.pop(0)
        assert item is not self

        self.send_to(item)
        head = item

        while len(chain_list):
            item = chain_list.pop(0)
            head.send_to(item)
            head = item

        return (self, item)

    def signal(self, event, start_time, end_time):
        """
        Fires the beat or note events down through the chain.
        Do not reimplement signal in subclasses - only on_signal
        """

        evt = event.copy()
        if self.channel is not None:
            evt.channel = self.channel

        should_run = next(self.when)

        if should_run:
            return self.on_signal(evt, start_time, end_time)
        else:
            # bypass THIS plugin and fire the sends directly
            # on_signal does not have a chance to run.
            results = []
            evt.keep_alive = True
            for send in self.sends:
                results.append(send.signal(evt, start_time, end_time))
            if len(results) > 0:
                return results
            else:
                return [ event ]

    def on_signal(self, event, start_time, end_time):
        """
        Override this pattern in each plugin, with variations, and return
        the list of events produced
        """

        # see scale_follower for a good example
        raise NotImplementedError
