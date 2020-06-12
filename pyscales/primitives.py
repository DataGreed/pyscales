


class Note:
    """
    Represents a musical note
    """

    VALID_NOTE_NAMES = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

    SHARP_SYMBOL = "#"
    FLAT_SYMBOL = "b"

    NOTE_NAME_SHARP_TO_FLAT_SYNONYMS = {

    }

    NOTE_NAME_FLAT_TO_SHARP_SYNONYMS = {  # bemol

    }

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

    # TODO: method to return synonym name

    @classmethod
    def any_to_sharp_name(cls, note_name):
        if cls.FLAT_SYMBOL in note_name:
            return cls.NOTE_NAME_SHARP_TO_FLAT_SYNONYMS[note_name]
        else:
            return note_name

    @classmethod
    def sharp_to_flat_name(cls, note_name):
        return cls.NOTE_NAME_SHARP_TO_FLAT_SYNONYMS[note_name]

    @classmethod
    def flat_to_sharp_name(cls, note_name):
        return cls.NOTE_NAME_FLAT_TO_SHARP_SYNONYMS[note_name]


class ScaleFormula:
    """
    Represents a tonal formula that is used to build up a scale
    from any given root note
    """

class Scale:
    """
    Represents a musical scale
    """
    pass


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