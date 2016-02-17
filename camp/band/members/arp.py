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

from camp.band.members.member import Member

class Arp(Member):

    """
    A powerful arpeggiator.

    When done, will be able to move by scale notes, octaves, and semitones,
    and also have both a free and locked mode.

    The various transpositions can have different lengths, for instance, a 5 note
    semitone arpeggiation pattern can transpose every second note by +2 octaves.
    As such, this arp can be pretty chaotic.

    Locked will reset with each incoming note signal, free will run regardless
    of the incoming note signal.

    This is, therefore, somewhat of a mashup of subdivide.py and transpose.py,
    with some extra features.
    """

    def __init__(self, channel=None, splits=None, semitones=None, octaves=None, scale_notes=None, rests=None, mode='locked'):

        """
        Usage:

        - channel - MIDI channel to override, if any
        - semitones - offset by this many semitones for every arp note
        - octaves - offset by this many octaves for every arp note
        - scale_notes - offset by this many scale notes for every arp note (scale dependent)
        - rests - where this is true, do not play any notes
        - splits - decides how many arp notes to play inside each beat.  length=1 with no shifts is a no-op.
        - mode - if 'free', doesn't reset the arpeggiator with each beat.  Default 'locked', does.

        sd = Arp(
            splits=Endlessly[4],
            semitones=Endlessly[1,4,9],
            mode='free',
            rests=Endlessly[0,0,0,0,1]
            lengths=
        )

        # beat Fires
        # arp plays note+1, note+4, note+9, then note+1 semitones in sequence
        # beat Fires
        # arp plays REST, note+9, note+1, then note+4 semitones in sequence
        # beat Fires
        # arp plays note+9, note+1, then, note+9 semitones in sequence

        """

        super().__init__(channel=channel)

        print("ARP CH=%s" % self.channel)


        assert mode in [ 'free', 'locked']
        self._mode = mode

        # save the inputs (which might be selectors or just arrays) since if we are in 'locked'
        # mode we want to reset them at the beginning of each new beat.
        self._splits = splits
        self._semitones = semitones
        self._octaves = octaves
        self._scale_notes = scale_notes
        self._rests = rests

        self.current_scale = None
        self.previous_scale = None
        self.working_scale = None
        self._subdivide_amounts = self.draw_from(splits)
        self._run_once = True

    def _scale_note_shift(self, scale_note_shift=None, note=None):
        raise NotImplementedError()

    def _handle_arp_note(self, event):

        octave_shift = next(self._octave_amounts)
        semitone_shift = next(self._semitone_amounts)
        scale_shift = next(self._scale_amounts)

        # FIXME: this copy may not be needed because of event.copy
        #notes = [ n.copy() for n in event.notes ]
        # if so, also remove from subdivide
        rest = next(self._rests_cond)

        if rest:
            print("ARP RESTING because %s" % rest)
            event.notes = []
        else:
            print("ARP GOT NOTES: %s" % event.notes)
            if len(event.notes) == 0:
                return
                #raise Exception("ow?")
            for (i,note) in enumerate(event.notes):
                if octave_shift:
                    print("ARP:OS")
                    event.notes[i] = note.transpose(octaves=octave_shift)
                if semitone_shift:
                    print("ARP:OS")
                    event.notes[i] = note.transpose(semitones=semitone_shift)
                if scale_shift:
                    print("ARP:OS")
                    event.notes[i] = self._scale_note_shift(scale_note_shift=scale_shift, note=note)

    def on_signal(self, event, start_time, end_time):

        produced = []

        """
        Callback for the plugin.  This one is a bit complicated.
        """

        if self._scale_notes:
            self.current_scale = event.get('scale', None)
            if self.current_scale is None:
                raise Exception("requires scale data to arpeggiate on scale")
            # aside:
            # this new scale isn't SUPER huge for calculations so if you need to do something crazy like
            # jump around 5 octaves and also shift by scale notes, do it like this:
            # Arp(scale_notes=Endlessly([-2,0,2]), octaves=Endlessly([-5,5]))
            # NOT:
            # Arp(scale_notes=Endlessly([100,0,80,-36)])
            # as that will probably make stuff blow up and I can't be bothered with the error handling ATM.
            self.working_scale_notes = [ note.transpose(octaves=-3) for note in scale.copy.generate(length=12*6) ]

        if (self.current_scale != self.previous_scale) or self._mode == 'locked' or self._run_once is False:
            print("ARP RESET")
            self._run_once = True
            self._octave_amounts = self.draw_from(self._octaves)
            self._semitone_amounts = self.draw_from(self._semitones)
            self._scale_amounts = self.draw_from(self._scale_notes)
            self._rests_cond = self.draw_from(self._rests)
            self.previous_scale = self.current_scale

        # FIXME: lots of repeated code with subdivide, let's make this share code!!!

        # calculate the length of the beat cycle
        delta = end_time - start_time
        # find out how many subdivisions there are for this beat
        slices = next(self._subdivide_amounts)
        # how long is each subdivision in seconds?
        each_slice_width = delta / slices
        # when does the first subdivision start?
        new_start_time = start_time

        # here we flag the note. This is because certain plugins like
        # ScalePlayer need to know what to do such that they shorten
        # the durations of the notes coming out, otherwise things won't work right.

        event.add_flags(subdivide=slices)

        # for however many times we are going to subdivide

        for slice_num in range(0,slices):

            new_event = event.copy()

            # calculate the end time of the new beat we are going to trigger

            new_end_time = new_start_time + each_slice_width
            new_event.time = new_start_time

            self._handle_arp_note(new_event)

            for send in self.sends:
                send.signal(new_event, new_start_time, new_end_time)

            # move on to the next beat in the subdivision.
            new_start_time = new_start_time + each_slice_width

            produced.append(new_event)

        return produced
