from copy import copy

from .primitives import Note, NoteArray, Scale, ToneDelta


class PianoKey:
    """
    Represents a piano keyboard key
    """
    # w	b	w	b	w	w	b	w	b	w	b	w
    WHITE_KEYS = [True, False, True, False, True, True, False, True, False, True, False, True]
    BLACK_KEYS = [not x for x in WHITE_KEYS]

    KEYS_IN_OCTAVE = 12

    DEFAULT_NOTES_ORDER = NoteArray(NoteArray.DEFAULT_NOTE_ORDER)

    def __init__(self, key_number: int, octave_number: int = 0):
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

        # find and save original note that should be played with this key
        self.original_note = copy(self.DEFAULT_NOTES_ORDER[key_number-1]) # key number is zero-based
        self.original_note.octave_number = octave_number

        self.tuned_note = copy(self.original_note)

    def white(self):
        return self.WHITE_KEYS[self.key_number-1]  # key number is zero-based

    def black(self):
        return not self.white()

    def note(self) -> Note:
        return copy(self.tuned_note)

    def tune(self, semitones, use_original_note=True):
        """
        Tunes note played by this key by number of semitones provided.
        :param semitones: number of semitones to shift note, can be negative
        :param use_original_note: if true, tunes relative to the original note set to this key.
        If False, tunes relative to the last tuned note.
        :return:
        """
        if use_original_note:
            self.tuned_note = self.original_note + ToneDelta(semitones=semitones)
        else:
            self.tuned_note += ToneDelta(semitones=semitones)


class PianoKeyboard:
    """
    Represents a piano keyboard
    """
    def __init__(self, number_of_keys: int, first_key_number: int, first_octave_number: int=0):
        """

        :param number_of_keys:
        :param first_key_number: first key, 1-based
        :param first_octave_number:
        """
        self.__semitones_tuned = 0
        self.first_key_number=first_key_number
        self.first_octave_number = first_octave_number


        self.keys = []

        current_number_in_octave = first_key_number
        current_octave=first_octave_number

        for i in range(number_of_keys):
            self.keys.append(PianoKey(key_number=current_number_in_octave, octave_number=current_octave))
            current_number_in_octave +=1

            if current_number_in_octave> PianoKey.KEYS_IN_OCTAVE:
                current_number_in_octave = 0
                current_octave +=1

    def tune(self, semitones: int):
        """
        Tunes the entire keyboard by number of semitones from default.
        Useful if you want to transapose keys from one layout to another.
        E.g. play some scale with all white keys (other than C major or A minor)
        :param semitones:
        :return:
        """
        self.__semitones_tuned = semitones

        for key in self.keys:
            key.tune(semitones=semitones, use_original_note=True)

    def get_keys_for_scale(self, scale: Scale):
        pass

    def render_keys_in_ascii(self):
        pass

    def render_notes_in_ascii(self):
        pass

    def render_scale_in_ascii(self, scale: Scale):
        pass