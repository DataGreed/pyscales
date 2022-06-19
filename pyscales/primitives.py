import math
from copy import copy
from typing import Optional

from pyscales import constants


class ToneDelta:
    """
    Represents difference between notes in semitones
    """
    def __init__(self, semitones: int):
        self.semitones = semitones


    def __eq__(self, other):

        return self.semitones == other.semitones

    def __add__(self, other):

        return ToneDelta(self.semitones + other.semitones)

    def __sub__(self, other):
        return ToneDelta(self.semitones + other.semitones)

    def __mul__(self, other):

        if isinstance(other, int):

            return ToneDelta(self.semitones * other)

        raise ValueError("Can only multiply by integer")

    def __str__(self):

        return f"d{self.semitones}"

    def __repr__(self):

        return f"<ToneDelta {self.semitones}>"


class Note:
    """
    Represents a musical note
    """

    VALID_NOTE_NAMES = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

    SHARP_SYMBOL = "#"
    FLAT_SYMBOL = "b"

    NOTE_NAME_SHARP_TO_FLAT_SYNONYMS = {
        "C#": "Db",
        "D#": "Eb",
        "F#": "Gb",
        "G#": "Ab",
        "A#": "Bb",
    }

    # bemol
    NOTE_NAME_FLAT_TO_SHARP_SYNONYMS = {y:x for x,y in NOTE_NAME_SHARP_TO_FLAT_SYNONYMS.items()}

    def __init__(self, note_name: Optional[str]=None, octave_number:int = 0, midi_value:Optional[int] = None):  # FIXME:should we use 4 octave as default? will NoteArray still work properly?

        if note_name and midi_value:
            raise ValueError("Specify either a note name or midi value, not both.")

        if (midi_value is None) and (not note_name):
            raise ValueError("Specify either a note name or midi value")

        if midi_value:
            if (midi_value < constants.MIDI_LOWEST_NOTE_VALUE) or (midi_value > constants.MIDI_HIGHEST_NOTE_VALUE):
                raise ValueError(f"MIDI note value {midi_value} is not "
                                 f"in {constants.MIDI_LOWEST_NOTE_VALUE}...{constants.MIDI_HIGHEST_NOTE_VALUE} range")

            note_name = self.get_note_name_from_midi_value(midi_value)
            octave_number = self.get_octave_from_midi_value(midi_value)


        note_name = note_name[0].upper() + note_name[1:]

        if note_name not in self.VALID_NOTE_NAMES:
            raise ValueError(f"Invalid note name {note_name}. Valid names include: {', '.join(self.VALID_NOTE_NAMES)}")

        self.note_name = self.any_to_sharp_name(note_name)

        # if octave_number < constants.LOWEST_OCTAVE_NUMBER or octave_number>constants.HIGHEST_OCTAVE_NUMBER:
        # TODO: should we really validate this here? It only makes sense foro midi octave numbering
        ## fixme: this breaks NoteAray warping calculations now. Fix it and still have a value check
        #     raise ValueError(f"Octave number {octave_number} is not "
        #                      f"within {constants.LOWEST_OCTAVE_NUMBER}...{constants.HIGHEST_OCTAVE_NUMBER} range")

        self.octave_number = octave_number

    def __eq__(self, other):

        return self.note_name == other.note_name and self.octave_number == other.octave_number

    def __add__(self, other):

        from pyscales import IntervalInScale
        from pyscales import Interval
        if isinstance(other, IntervalInScale):
            return other.add_to_note(self)
        elif isinstance(other, Interval):
            return other.add_to_note(self)

        # assume other is ToneDelta
        # TODO: cache this somewhere
        notes_order = NoteArray(NoteArray.DEFAULT_NOTE_ORDER)

        try:
            this_note_index = notes_order.index(self)

            return notes_order[this_note_index+other.semitones]

        except AttributeError:
            raise ValueError("Use ToneDelta objects to add and subtract notes")

    def __sub__(self, other):

        # TODO: cache this somewhere
        notes_order = NoteArray(NoteArray.DEFAULT_NOTE_ORDER)

        this_note_index = notes_order.index(self)

        from pyscales import IntervalInScale

        from pyscales import Interval
        if hasattr(other, 'semitones'):

            return notes_order[this_note_index-other.semitones]

        elif isinstance(other, Note):

            other_not_index = notes_order.index(other)

            return ToneDelta(this_note_index-other_not_index)

        elif isinstance(other, IntervalInScale):

            return other.subtract_from_note(self)

        elif isinstance(other, Interval):
            return other.subtract_from_note(self)

        raise ValueError("Can only subtract ToneDelta, IntervalInScale or other Note")


    def __str__(self):

        return f"{self.note_name}{self.octave_number}"

    def __repr__(self):

        return f"<Note {self}>"

    # TODO: method to return synonym name

    @classmethod
    def any_to_sharp_name(cls, note_name):
        if cls.FLAT_SYMBOL in note_name:
            return cls.NOTE_NAME_FLAT_TO_SHARP_SYNONYMS[note_name]
        else:
            return note_name

    @classmethod
    def sharp_to_flat_name(cls, note_name):
        return cls.NOTE_NAME_SHARP_TO_FLAT_SYNONYMS[note_name]

    @classmethod
    def flat_to_sharp_name(cls, note_name):
        return cls.NOTE_NAME_FLAT_TO_SHARP_SYNONYMS[note_name]

    @property
    def frequency(self):
        """
        Calculates and returns the frequency of the note.
        Uses fundamental note frequency defined in constants.

        Base on a formula from https://pages.mtu.edu/~suits/NoteFreqCalcs.html
        """
        if (self.note_name == constants.FUNDAMENTAL_NOTE_NAME) and (self.octave_number == constants.FUNDAMENTAL_NOTE_OCTAVE):
            return constants.FUNDAMENTAL_NOTE_FREQUENCY

        # TODO: pre-calculate all note frequencies on init? Or at least chache them
        # TODO: cache fundamental note somewhere for faster calculations
        fundamental_note = Note(constants.FUNDAMENTAL_NOTE_NAME, constants.FUNDAMENTAL_NOTE_OCTAVE)
        halfsteps_away_from_fund_note = (self - fundamental_note).semitones

        frequency = constants.FUNDAMENTAL_NOTE_FREQUENCY*(constants.TWELFTH_ROOT_OF_TWO**halfsteps_away_from_fund_note)

        # print(f"frequency debug: {locals()}")

        return frequency

    @property
    def midi_value(self):
        """
        Returns midi note value (number) for this note.
        """

        # I derived this formula looking at midi note numbers here:
        # https://musicinformationretrieval.com/midi_conversion_table.html
        # not sure if that's correct so we have to test it just in case

        midi_number = 12*(self.octave_number+1) + constants.DEFAULT_NOTE_NAME_ORDER_IN_MIDI_OCTAVE.index(self.note_name)

        if midi_number > constants.MIDI_HIGHEST_NOTE_VALUE or midi_number<constants.MIDI_LOWEST_NOTE_VALUE:
            raise ValueError(f"Note {self} is out of MIDI range (11-132)")

        return midi_number

    @staticmethod
    def get_note_name_from_midi_value(midi_value):
        # I derived this from looking on midi value table, have to check
        return constants.DEFAULT_NOTE_NAME_ORDER_IN_MIDI_OCTAVE[midi_value % 12]

    @staticmethod
    def get_octave_from_midi_value(midi_value):
        return math.floor(midi_value / 12) - 1


class NoteArray:
    """
    Structure that returns notes based on supplied indexes.
    Supports wrapping around and octaves.
    Zero-based.
    Supports splices.
    Note that negative indexes may represent notes
    from negative octaves.

    Based on https://stackoverflow.com/questions/22122623/
    """

    # IMPORTANT: note that octave numbering always starts with C, does not matter which scale you're using.
    DEFAULT_NOTE_ORDER = [Note("c"),
             Note("c#"), Note("d"), Note("d#"), Note("e"),
             Note("f"), Note("f#"), Note("g"), Note("g#"),
            Note("a"), Note("a#"), Note("b")]

    def __init__(self, notes=None, simulate_octaves=True):
        """
        :param notes: list of ordered notes. If not specified, uses notes in default order
        starting from C0
        """
        self.notes = notes or copy(self.DEFAULT_NOTE_ORDER)

        # this may work unpredictably if notes are not in order or if they are having different octaves
        # that are not following each other.
        # note array assumes that notes are more or less in order (left to right - low to high)
        self.simulate_octaves = simulate_octaves

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index):

        if isinstance(index, slice):
            # Get the start, stop, and step from the slice
            # return [self[ii] for ii in range(*index.indices(10*9))]
            return [self[ii] for ii in range(index.start, index.stop)]

        elif isinstance(index, int):

            normalized_index = index % len(self.notes)

            octave_shift = 0

            # NoteArray assumes that notes holds one octave
            # if the supplied index is out of bounds and is higher than the notes length,
            # it goes N octaves up. If it's lower - N octaves down.
            if (index<0 or index >= len(self.notes) ) and self.simulate_octaves:
                octave_shift = (index- normalized_index) / len(self.notes)


            normalized_note = self.notes[normalized_index]

            return Note(note_name=normalized_note.note_name, octave_number=int(normalized_note.octave_number+octave_shift))

    def index(self, note:Note):
        return self.get_note_index(note)

    def get_note_index(self, note:Note):
        # TODO: implement! don't forget to take octave in account if enabled
        pass

        if self.simulate_octaves:

            # FIXME: note that this part of code creates notes in some weird negative octaves
            #  which should not be done at all as it breaks validation of octave umbers when creating notes
            #  and has to be fixed.

            # TODO: fix: there should be much better way to find it knowing the octave
            # than just iterating
            return self[-300:300].index(note) - 300 # index can be negative

        return self.notes.index(note)

    def __str__(self):

        return " ".join([str(x) for x in self.notes])





