
class FxBuses(object):

    __slots__ = [ '_busses', '_factory' ]

    def __init__(self):
        self._busses = dict()

    def set(self, **busses):

        def callback(song):
            for (bus_name, bus) in busses:
                if not isinstance(bus, FxBus):
                    raise Exception("only a FxBus is allowed inside of FxBusses set method")
                self._busses[bus_name] = bus
            return self

        return callback
