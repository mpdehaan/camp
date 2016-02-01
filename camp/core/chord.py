class Note(object):

    def __init__(self, name=None, octave=None, rest=False):

        assert name is not None
        assert octave is not None

        self.name = name
        self.octave = octave
        self.rest = False


