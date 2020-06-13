from .primitives import Note, NoteArray, Scale


class PianoKey:
    """
    Represents a piano keyboard key
    """
    # w	b	w	b	w	w	b	w	b	w	b	w
    WHITE_KEYS = [True, False, True, False, True, True, False, True, False, True, False, True]
    BLACK_KEYS = [not x for x in WHITE_KEYS]

    DEFAULT_NOTES = []

    KEYS_IN_OCTAVE = 12

    def __init__(self, key_number: int, octave_number: int = 0, note: Note=None):
        """

        :param key_number: number of key in octave, 1-based
        :param octave_number: octave number, can be negative
        :param note: not to play when pressed
        """

        # TODO: should octaves have relative-based numbering or?..
        # of we can use midi numbers
        # https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
        # https://ultimatemusictheory.com/piano-key-numbers/
        # should default octave be 4 and disallow negative octaves?
        if key_number < 1 or key_number > self.KEYS_IN_OCTAVE:

            raise ValueError(f"Piano key number should be between 1 "
                             f"and {self.KEYS_IN_OCTAVE} (inclusive), not {key_number}")

        self.key_number = key_number
        self.octave_number = octave_number
        self.original_note = note
        self.tuned_note = note


    # todo: tune method

class PianoKeyboard:
    """
    Represents a piano keyboard
    """
    def __init__(self, number_of_keys: int, first_key_number: int, first_octave_number: int):
        """

        :param number_of_keys:
        :param first_key_number: first key, 1-based
        :param first_octave_number:
        """
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