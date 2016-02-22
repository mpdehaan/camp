
class Instruments(object):

    __slots__ = [ "_instruments", "_factory" ]

    def __init__(self):
        self._instruments = dict()

    def set(self, **kwargs):

        def callback(song):
            for (instrument_name, midi_channel) in kwargs.items():
                if type(midi_channel) != int:
                    raise Exception("instrument midi channel requires an integer")
                    self._instruments[instrument_name] = midi_channel
            return self
        return callback
