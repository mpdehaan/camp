# ==============================================================================
# constants - http://pydoc.net/Python/python-rtmidi/0.4b/rtmidi.midiconstants/

NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
NOTE_ON = 0x90
# 1001cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
POLYPHONIC_PRESSURE = AFTERTOUCH = 0xA0
# 1010cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
CONTROLLER_CHANGE = 0xB0 # see Channel Mode Messages!!!
# 1011cccc 0ccccccc 0vvvvvvv (channel, controller, value)
PROGRAM_CHANGE = 0xC0
# 1100cccc 0ppppppp (channel, program)
CHANNEL_PRESSURE = 0xD0
# 1101cccc 0ppppppp (channel, pressure)
PITCH_BEND = 0xE0
# 1110cccc 0vvvvvvv 0wwwwwww (channel, value-lo, value-hi)
NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
NOTE_ON = 0x90
# ==============================================================================
