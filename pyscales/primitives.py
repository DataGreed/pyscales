from copy import copy


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

    Based on https://stackoverflow.com/questions/22122623/
    """
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


class ScaleFormula:
    """
    Represents a tonal formula that is used to build up a scale
    from any given root note
    """

    def __init__(self, formula:str, name:str="Unnamed"):




        self.formula = formula
        self.note_map = self.note_map_from_formula_string(formula)
        self.name = name

    @classmethod
    def note_map_from_formula_string(cls, formula: str):
        result = [True] # root note is always played
        for char in formula:
            if char.lower() in ['w', 't']:  # whole tone
                result+=[False, True]  # skip one semitone, map semitone that goes next
            elif char.lower() in ['h', 's']:    # half tone/ semitone
                result.append(True) # map next semitone
            else:
                raise ValueError()

        return result


class Scale:
    """
    Represents a musical scale
    """

    DEFAULT_NOTE_ORDER = [Note("a"), Note("a#"), Note("b"), Note("c"),
                          Note("c#"), Note("d"), Note("d#"), Note("e"),
                          Note("f"), Note("f#"), Note("g"), Note("g#")]

    def __init__(self, root_note:Note, formula: ScaleFormula):

        self.root_note = root_note
        self.formula = formula

        self._all_notes = NoteArray(self.DEFAULT_NOTE_ORDER)

    def notes_in_scale(self) -> NoteArray:

        # find root note index
        i = self._all_notes.index(self.root_note)

        result_array = []

        for used_in_scale in self.formula.note_map:

            if used_in_scale:
                result_array.append(copy(self._all_notes[i]))

            i+=1

            # TODO: wrap octave around !

        return NoteArray(result_array)


    def notes_not_in_scale(self):
        pass


    def __str__(self):
        # TODO: change flats and sharps so note names will be unique across scale
        return str(self.notes_in_scale())


class PianoKey:
    """
    Represents a piano keyboard key
    """
    # w	b	w	b	w	w	b	w	b	w	b	w
    WHITE_KEYS = [True, False, True, False, True, True, False, True, False, True, False, True]
    BLACK_KEYS = [not x for x in WHITE_KEYS]

    DEFAULT_NOTES = []

    KEYS_IN_OCTAVE = 12

    def __init__(self, key_number: int, octave_number: int = 0):
        """

        :param key_number: number of key in octave, 1-based
        :param octave_number: octave number, can be negative
        """

        # TODO: should octaves have relative-based numbering or?..
        # of we can use midi numbers
        # https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
        # https://ultimatemusictheory.com/piano-key-numbers/
        # shpould default octave be 4 and disallow negative octaves?
        if key_number < 1 or key_number > self.KEYS_IN_OCTAVE:

            raise ValueError(f"Piano key number should be between 1 "
                             f"and {self.KEYS_IN_OCTAVE} (inclusive), not {key_number}")

        self.key_number = key_number
        self.octave_number = octave_number


    # todo: tune method

class PianoKeyboard:
    """
    Represents a piano keyboard
    """
    def __init__(self, number_of_keys: int, first_key_number: int, first_octave_number: int):

        self.__semitones_tuned = 0

        pass

    def tune(self, semitones: int):
        """
        Tunes the entire keyboard by number of semitones from default.
        Useful if you want to transapose keys from one layout to another.
        E.g. play some scale with all white keys (other than C major or A minor)
        :param semitones:
        :return:
        """
        self.__semitones_tuned = semitones
        # TODO: implement
        pass

    def get_keys_for_scale(self, scale: Scale):
        pass

    def render_keys_in_ascii(self):
        pass

    def render_notes_in_ascii(self):
        pass

    def render_scale_in_ascii(self, scale: Scale):
        pass