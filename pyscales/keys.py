from copy import copy

from .primitives import Note, NoteArray, ToneDelta
from .scales import Scale


class PianoKey:
    """
    Represents a piano keyboard key
    """
    # w	b	w	b	w	w	b	w	b	w	b	w
    WHITE_KEYS = [True, False, True, False, True, True, False, True, False, True, False, True]
    BLACK_KEYS = [not x for x in WHITE_KEYS]

    KEYS_IN_OCTAVE = 12

    # keyboards
    DEFAULT_NOTES_ORDER_LIST = [ Note("c"), Note("c#"), Note("d"),
                                 Note("d#"), Note("e"), Note("f"),
                                 Note("f#"), Note("g"), Note("g#"),
                                 Note("a"), Note("a#"), Note("b")]

    DEFAULT_NOTES_ORDER = NoteArray(DEFAULT_NOTES_ORDER_LIST)

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

    def render_key_in_ascii(self):

        return " □  " if self.white() else " ▩  "

    def render_note_in_ascii(self, render_octave=True):
        # TODO: control note name selection fron synonims

        note_label = self.note().note_name
        if render_octave:
            note_label += str(self.note().octave_number)

        result = f" {note_label}"

        # needs to be four chars wide to align with keys
        if len(result) < 4:
            result += " " * (4-len(result))
        return result

    def render_blank_note_in_ascii(self):
        """
        renders blank space instead of note
        :return:
        """
        return " " * 4


class PianoKeyboard:
    """
    Represents a piano keyboard
    """
    def __init__(self, number_of_keys: int, first_key_number: int, first_octave_number: int=0, name="Unnamed"):
        """

        :param number_of_keys:
        :param first_key_number: first key, 1-based
        :param first_octave_number:
        """
        self.__semitones_tuned = 0
        self.first_key_number=first_key_number
        self.first_octave_number = first_octave_number

        self.name = name

        self.keys = []

        current_number_in_octave = first_key_number
        current_octave=first_octave_number

        for i in range(number_of_keys):
            self.keys.append(PianoKey(key_number=current_number_in_octave, octave_number=current_octave))
            current_number_in_octave +=1

            if current_number_in_octave> PianoKey.KEYS_IN_OCTAVE:
                current_number_in_octave = 1 # 1-based
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
        """
        Returns array of keys that correspond to given scale
        :param scale:
        :return:
        """
        result = []

        for key in self.keys:

            if scale.is_in_scale(key.note()):

                result.append(key)

        return result

    def render_keys_in_ascii(self):

        result = ""
        for key in self.keys:
            result += key.render_key_in_ascii()
        return result

    def render_notes_in_ascii(self, render_octave_number=True):

        result = ""
        for key in self.keys:
            result += key.render_note_in_ascii(render_octave=render_octave_number)
        return result

    def render_note_scale_in_ascii(self, scale: Scale, render_octave_number=True):

        result = ""

        for key in self.keys:

            if scale.is_in_scale(key.note()):

                result += key.render_note_in_ascii(render_octave=render_octave_number)
            else:

                result += key.render_blank_note_in_ascii()

        return result

    def copy(self):
        return copy(self)
