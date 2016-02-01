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

SCALE_TYPES = dict(
   major         = [ 1, 2, 3,    4, 5, 6,    7,    8 ], 
   natural_minor = [ 1, 2, 'b3', 4, 5, 'b6', 'b7', 8 ],
)

from camp.core.note import note, Note

class Scale(object):

    def __init__(self, root=None, typ=None):

        """
        Constructs a scale:

	scale = Scale(root='C4', typ='major')
        """

        assert root is not None
        assert typ is not None
        if isinstance(root, str):
            root = note(root) 
        self.root = root
        self.typ = typ

    def generate(self, length=None):
        """
        Allows traversal of a scale in a forward direction.
        Example:
        for note in scale.generate(length=2):
           print note
        """


        assert length is not None
        scale_data = SCALE_TYPES[self.typ][:]
        # remove the last scale note so we bump the octave at the right place
        # still following common music theory convention of including the tonic twice to avoid surprises
        # in scale definition
        scale_data.pop()

        octave_shift = 0
        index = 0
        while (length is None or length > 0):

            if index == len(scale_data):
               index = 0
               octave_shift = octave_shift + 1
            result = self.root.transpose(degrees=scale_data[index], octaves=octave_shift)
            yield(result)
            index = index + 1
            if length is not None:
                length = length - 1

    def __eq__(self, other):
        """
        Scales are equal if they are the ... same scale
        """
        return self.root == other.root and self.typ == other.typ

    def short_name(self):
        return "%s %s" % (self.root.short_name(), self.typ)

    def __repr__(self):
        return "Scale<%s>" % self.short_name()

def scale(input):
    """
    Shortcut: scale(['C major') -> Scale object
    """
    (root, typ) = input.split()
    return Scale(root=note(root), typ=typ)

