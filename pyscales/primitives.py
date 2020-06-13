from copy import copy


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

    def __init__(self, note_name: str, octave_number:int = 0):

        note_name = note_name[0].upper() + note_name[1:]

        if note_name not in self.VALID_NOTE_NAMES:
            raise ValueError(f"Invalid note name {note_name}. Valid names include: {', '.join(self.VALID_NOTE_NAMES)}")

        self.note_name = self.any_to_sharp_name(note_name)
        self.octave_number = octave_number

    def __eq__(self, other):

        return self.note_name == other.note_name and self.octave_number == other.octave_number

    def __add__(self, other):

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

        if hasattr(other, 'semitones'):

            return notes_order[this_note_index-other.semitones]

        elif isinstance(other, Note):

            other_not_index = notes_order.index(other)

            return ToneDelta(this_note_index-other_not_index)

        raise ValueError("Can only subtract ToneDelta or other Note")


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
    # TODO: is there any use starting it with a? Should we start it with c instead? Won't it break octave wrapping?
    DEFAULT_NOTE_ORDER = [Note("a"), Note("a#"), Note("b"), Note("c"),
             Note("c#"), Note("d"), Note("d#"), Note("e"),
             Note("f"), Note("f#"), Note("g"), Note("g#")]

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
            # TODO: fix: there should be much better way to find it knowing the octave
            # than just iterating
            return self[-300:300].index(note) - 300 # index can be negative

        return self.notes.index(note)

    def __str__(self):

        return " ".join([str(x) for x in self.notes])





