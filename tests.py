import unittest

from pyscales import constants, scaleformulas
from pyscales.primitives import Note, NoteArray
from pyscales.scales import Scale


class TestNoteFrequencies(unittest.TestCase):


    def test_fundamental_frequency(self):

        a4 = Note("A", 4)
        self.assertEqual(a4.note_name, "A")
        self.assertEqual(a4.octave_number, 4)
        self.assertEqual(a4.frequency, constants.FUNDAMENTAL_NOTE_FREQUENCY)

    def test_fundamental_frequency_a440(self):
        a4 = Note("A", 4)
        self.assertEqual(a4.note_name, "A")
        self.assertEqual(a4.octave_number, 4)
        self.assertEqual(a4.frequency, constants.FUNDAMENTAL_NOTE_FREQUENCY)
        self.assertEqual(a4.frequency, 440)

    def test_frequency_of_various_notes_in_a440_tuning(self):

        notes = [
            ["A", 5, 880],
            ["C", 5, 523.25],
            ["C", 6, 1046.5],
            ["F#", 2, 92.5],
            ["A", 1, 55],
            ["G", 1, 49],
            ["G", 4, 392],
            ["F", 5, 698.46],
        ]

        for line in notes:

            n = Note(line[0], line[1])
            self.assertEqual(n.note_name, line[0])
            self.assertEqual(n.octave_number, line[1])
            self.assertAlmostEqual(n.frequency, line[2], places=2)


class ScalesAndModesTestCase(unittest.TestCase):

    def test_modes(self):

        scale = Scale(Note("A", 3), scaleformulas.NATURAL_MINOR_FORMULA)
        expected_note_names=list("ABCDEFG")

        for i in range(len(expected_note_names)):

            self.assertEqual(scale.notes_in_scale()[i].note_name, expected_note_names[i])

        scale = Scale(Note("F", 3), scaleformulas.LYDIAN_FORMULA)
        expected_note_names = list("FGABCDE")

        for i in range(len(expected_note_names)):
            self.assertEqual(scale.notes_in_scale()[i].note_name, expected_note_names[i])

        scale = Scale(Note("G", 3), scaleformulas.PHRYGIAN_FORMULA)
        expected_note_names = ["G", "G#", "A#", "C", "D", "D#", "F"]

        for i in range(len(expected_note_names)):
            self.assertEqual(scale.notes_in_scale()[i].note_name, expected_note_names[i])


class MidiNoteValuesTest(unittest.TestCase):

    def test_midi_values_from_notes(self):

        # base on https://musicinformationretrieval.com/midi_conversion_table.html
        # although this document mentions non-existent B#9 - typo?

        test_data = [
            ["C", 4, 60],
            ["D#", 5, 75],
            ["G#", 5, 80],
            ["E", 0, 16],
            ["A#", 2, 46],
            ["B", 3, 59],
            ["A", 4, 69],
            ["G", 5, 79],
            ["B", 9, 131],
        ]

        for line in test_data:
            self.assertEqual(Note(line[0],line[1]).midi_value, line[2])

    def test_initializing_notes_from_midi_values(self):

        test_data = [
            ["C", 4, 60],
            ["D#", 5, 75],
            ["G#", 5, 80],
            ["E", 0, 16],
            ["A#", 2, 46],
            ["B", 3, 59],
            ["A", 4, 69],
            ["G", 5, 79],
            ["B", 9, 131],
        ]

        for line in test_data:
            note = Note(midi_value=line[2])

            self.assertEqual(note.note_name, line[0])
            self.assertEqual(note.octave_number, line[1])


if __name__ == '__main__':
    unittest.main()
