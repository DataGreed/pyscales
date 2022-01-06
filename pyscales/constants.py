# frequency of note A4 for equal temperament (the only temprament supported by this lib, at least for now)
FUNDAMENTAL_NOTE_NAME = "A"
FUNDAMENTAL_NOTE_OCTAVE = 4
FUNDAMENTAL_NOTE_FREQUENCY = 440  # hz

LOWEST_OCTAVE_NUMBER = 0
HIGHEST_OCTAVE_NUMBER = 9
# frequency ratio of semitone, see https://en.wikipedia.org/wiki/Twelfth_root_of_two
TWELFTH_ROOT_OF_TWO = 2**(1/12)
# used to calculated midi note values
DEFAULT_NOTE_NAME_ORDER_IN_MIDI_OCTAVE = ("C", "C#", "D", "D#", "E", "F", "F#", "G","G#", "A", "A#", "B")

MIDI_LOWEST_NOTE_VALUE = 11
MIDI_HIGHEST_NOTE_VALUE = 132
