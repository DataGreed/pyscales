from copy import copy

from .primitives import Note, NoteArray


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

        # last note in formula is always duplicated, we don;t need that in the map
        # if weleave it in, NoteArray will be giving wrong results when wrapping around
        return result[:-1]


class Scale:
    """
    Represents a musical scale
    """

    DEFAULT_NOTE_ORDER = [Note("c"),
                          Note("c#"), Note("d"), Note("d#"), Note("e"),
                          Note("f"), Note("f#"), Note("g"), Note("g#"),
                          Note("a"), Note("a#"), Note("b")]

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

    def is_in_scale(self, note: Note) -> bool:

        try:
            # try to find index in scale
            # TODO: cache notes_in_scale
            self.notes_in_scale().index(note)
            return True

        except ValueError:
            return False

    def scale_name(self):

        return f"{self.root_note.note_name} {self.formula.name}"

    def __str__(self):
        # TODO: change flats and sharps so note names will be unique across scale
        return str(self.notes_in_scale())