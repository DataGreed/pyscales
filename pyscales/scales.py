from copy import copy
from enum import Enum
from typing import Optional

from .primitives import Note, NoteArray, ToneDelta


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

    @property
    def all_notes(self):
        return self._all_notes


class IntervalQuality(Enum):
     PERFECT = 0
     MINOR = 1
     MAJOR = 2
     DIMINISHED = 3
     AUGMENTED = 4

     def name(self):
         return INTERVAL_QUALITY_NAMES[self]

     def short_name(self):
         return INTERVAL_QUALITY_SHORT_NAME[self]

     def notation(self):
         return INTERVAL_QUALITY_NOTATION[self]

# todo: also add scientific notations
INTERVAL_QUALITY_NAMES = {
    IntervalQuality.PERFECT: "Perfect",
    IntervalQuality.MINOR: "Minor",
    IntervalQuality.MAJOR: "Major",
    IntervalQuality.DIMINISHED: "Diminished",
    IntervalQuality.AUGMENTED: "Augmented",
}

INTERVAL_QUALITY_SHORT_NAME = {
    IntervalQuality.PERFECT: "perf",
    IntervalQuality.MINOR: "min",
    IntervalQuality.MAJOR: "maj",
    IntervalQuality.DIMINISHED: "dim",
    IntervalQuality.AUGMENTED: "aug",
}


# see https://en.wikipedia.org/wiki/Interval_(music)#Shorthand_notation
INTERVAL_QUALITY_NOTATION = {
    IntervalQuality.PERFECT: "P",
    IntervalQuality.MINOR: "m",
    IntervalQuality.MAJOR: "M",
    IntervalQuality.DIMINISHED: "d",
    IntervalQuality.AUGMENTED: "A",
}

# interval quality map
# based on https://en.wikipedia.org/wiki/Interval_(music)#Main_intervals
# They depend on staff position and quality
# there is logic behind it but its kind of complicated so it's easier to use this map
# to determine quality from staff positions and semitone difference.

# anyway, I would be glad if there was a more elegant way to determine interval quality.
# if an interval is compound, subtract 12 from semitones and 7 from staff position difference
# to use this map (test this!)
# map usage:
# INTERVAL_QUALITY_MAP[semitone_difference][staff_position_difference] -> IntervalQuality
INTERVAL_QUALITY_MAP = {
    # semitone difference as main dictionary key
    0: {
        # staff position _difference_, zero-based (0 for unison, 1 for second degree, 7 for octave, etc.)
        0: IntervalQuality.PERFECT,     # P1 - perfect unison
        1: IntervalQuality.DIMINISHED   # d2 - diminished second
    },
    1: {
        1: IntervalQuality.MINOR,       # m2 - minor second
        0: IntervalQuality.AUGMENTED    # A1 - augmented unison (not sure how it's possible)
    },
    2: {
        1: IntervalQuality.MAJOR,       # M2 - major second
        2: IntervalQuality.DIMINISHED   # d3 - diminished third
    },
    3: {
        2: IntervalQuality.MINOR,       # m3 - minor third
        1: IntervalQuality.AUGMENTED    # A2 - augmented second
    },
    4: {
        2: IntervalQuality.MAJOR,       # M3 - major third,
        3: IntervalQuality.DIMINISHED,  # d4 - diminished fourth
    },
    5: {
        3: IntervalQuality.PERFECT,     # P4 - perfect fourth
        2: IntervalQuality.AUGMENTED    # A3 - augmented third
    },
    6: {
        4: IntervalQuality.DIMINISHED,  # d5 - diminished 5th, tritone
        3: IntervalQuality.AUGMENTED,   # A4 - augmented fourth, tritone
    },
    7: {
        4: IntervalQuality.PERFECT,     #P5 - perfect fifth
        5: IntervalQuality.DIMINISHED,  #d6 - diminished 6th
    },
    8: {
        5: IntervalQuality.MINOR,       #m6 - minor sixth
        4: IntervalQuality.AUGMENTED,   #A5 - augmented fifth
    },
    9: {
        5: IntervalQuality.MAJOR,       #M6 - major sixth
        6: IntervalQuality.DIMINISHED,  #d7 - diminished 7th
    },
    10: {
        6: IntervalQuality.MINOR,       #m7 - minor seventh
        5: IntervalQuality.AUGMENTED    #A6 - augented sixth
    },
    11: {
        6: IntervalQuality.MAJOR,       #M7 - major seventh
        7: IntervalQuality.DIMINISHED   #d8 - diminished octave
    },
    12: {
        7: IntervalQuality.PERFECT,     #P8 - perfect octave
        6: IntervalQuality.AUGMENTED,   #A7 - augmented seventh
    }
}

# reverse map
INTERVAL_QUALITY_TO_SEMITONE_MAP = {
    # quality
    IntervalQuality.PERFECT: {
        # staff positions   # semitones
        0:                  0,
        3:                  5,
        4:                  7,
        7:                  12,
    },
    IntervalQuality.MAJOR: {
        # staff positions   # semitones
        1:                  2,
        2:                  4,
        5:                  9,
        6:                  11,
    },
    IntervalQuality.MINOR: {
        # staff positions   # semitones
        1:                  1,
        2:                  3,
        5:                  8,
        6:                  10,
    },
    IntervalQuality.DIMINISHED: {
        # staff positions   # semitones
        1:                  0,
        2:                  2,
        3:                  4,
        4:                  6,
        5:                  7,
        6:                  9,
        7:                  11,
    },
    IntervalQuality.AUGMENTED: {
        # staff positions   # semitones
        0:                  1,
        1:                  3,
        2:                  5,
        3:                  6,
        4:                  8,
        5:                  10,
        6:                  12,
    }
}


class IntervalInScale:
    """
    Use this to move up and down a scale by given number of staff positions.
    Add or subtract this to your notes.

    Not sure what's the correct name for this - degree? Interval in scale? Step?

    This entity is not quality-aware
    """

    def __init__(self, staff_positions: int, scale: Scale):
        self.staff_positions: int = staff_positions
        self.scale: Scale = scale

    def __add__(self, other):

        if isinstance(other, Note):

            try:
                note_index = self.scale.all_notes.index(other)

                # return corresponding note from scale
                return self.scale.all_notes[note_index+self.staff_positions].copy()

            except ValueError:
                raise ValueError(f"Note {other} is not in scale {self.scale}")

        elif isinstance(other, IntervalInScale):
            if other.scale == self.scale:
                return IntervalInScale(staff_positions=self.staff_positions+other.staff_positions)

            raise ValueError("Cannot add two IntervalInScale objects with different scales")

        else:
            raise ValueError("Can add IntervalInScale only to Note and other IntervalInScale")


    def __sub__(self, other):

        if isinstance(other, IntervalInScale):
            if other.scale == self.scale:
                return IntervalInScale(staff_positions=self.staff_positions + other.staff_positions)

            raise ValueError("Cannot add two IntervalInScale objects with different scales")

        else:
            raise ValueError("Can only subtract other IntervalInScale from IntervalInScale")


    def subtract_from_note(self, note: Note):

        interval_in_scale: IntervalInScale = copy(self)
        # invert for subtraction
        interval_in_scale.staff_positions -= interval_in_scale.staff_positions

        return interval_in_scale.__add__(note)

    def add_to_note(self, note):

        return self.__add__(note)


    # todo: add __sub__ method to note that calls this one with negative value

    # there is no __eq__ overload as it does not seem to make a lot of sense to compare this entities


class Interval:
    """
    Interval between notes.
    Characterized by quality. Not aware of scale.
    """

    # see https://en.wikipedia.org/wiki/Interval_(music)#Main_intervals
    # also https://en.wikipedia.org/wiki/Interval_(music)#Compound_intervals

    def __init__(self, staff_positions: int, quality: Optional[IntervalQuality] = None,
                                             semitones: Optional[int] = None):
        """
        @staff_positions - difference in staff positions  between notes. Zero-based.
        @quality - interval quality, depends on relation between staff positions and
                   semitone difference between two notes
        E.g. to get a Fifth, set this to 4
        see. https://en.wikipedia.org/wiki/Staff_(music)#Staff_positions
        """
        self.staff_positions: int = staff_positions

        if not quality and not semitones:
            raise ValueError("Provide either semitones or quality value")

        if quality and semitones:
            # if for some reason we were provided with both, check them instead of failing:
            assessed_quality = Interval.assess_quality(staff_positions, semitones)
            if assessed_quality != quality:
                raise ValueError(f"You passed both quality and semitones when defining Interval,"
                                 f"but quality {quality} does not correspond to {staff_positions} staff positions "
                                 f"with {semitones} semitones difference. Please provide either quality, or"
                                 f"semitones difference.")

        if quality:
            self.quality: IntervalQuality = quality
            self.semitones: int = semitones or Interval.calculate_semitones_difference(staff_positions, quality)

        elif semitones:
            self.semitones: int = semitones
            self.quality: IntervalQuality = quality or Interval.assess_quality(staff_positions, semitones)


    def get_tone_delta(self):
        """
        Returns a ToneDelta with the same number of semitones.
        Useful for adding or subtracting operations with Notes.
        """
        return ToneDelta(semitones=self.semitones)


    def __add__(self, other):
        if isinstance(other, Note):
            return self.add_to_note(other)

        # TODO: I am not sure that adding intervals together makes sense. Or does it?
        #  Do we add both semitones and staff positions?
        raise ValueError("You can only add Intervals to notes.")

    def add_to_note(self, note: Note) -> Note:
        """
        Adds this interval to a Note to get a new note
        """
        return note + self.get_tone_delta()

    def subtract_from_note(self, note: Note) -> Note:
        """
        Subtracts this interval to a Note to get a new note
        """
        return note - self.get_tone_delta()

    # def __sub__(self, other):
    #     # FIXME: should it be in Note?.. should we use some method in this class when calling it
    #     #  from note so logic will live here? should we just call __add__ with negative value from this class?
    #     raise NotImplementedError()
    #     pass

    def __eq__(self, other):

        if (other.staff_positions == self.staff_positions) and (other.quality == self.quality):
            return True

        return False


    def get_quantitative_name(self) -> str:

        # note that the interval name is 1-based, but the actual interval is 0-based
        # e.g. unison is called Perfect Unison and is written as P1 although notes are
        # 0 staff positions (and semitones) apart


        return str(self.staff_positions+1)

        # +1 because 1 staff position above something is 2nd e.g. "minor 2nd"

    def __str__(self):
        # TODO: make long notation option?
        return f"{self.quality.notation() if self.quality else '?'}{self.get_quantitative_name()}"


    @staticmethod
    def calculate_semitones_difference(staff_position_difference: int, quality: IntervalQuality) -> int:

        if staff_position_difference>7:
            staff_position_difference %= 7

        try:
            semitones = INTERVAL_QUALITY_TO_SEMITONE_MAP[quality][staff_position_difference]
        except KeyError:
            raise ValueError(f"Cannot find semitones difference corresponding "
                             f"to {quality.short_name()}{staff_position_difference+1} interval")

        return semitones

    @staticmethod
    def assess_quality(staff_position_difference: int, semitone_difference: int) -> IntervalQuality:
        """
        @staff_positions - staff positions between notes in scale
        @semitones - semitones between these notes
        """

        # basically it boils down to these rules:
        # https://music.utk.edu/theorycomp/courses/murphy/documents/Intervals.pdf
        # (thank you Dr. Barbara Murphy for a comprehensive explanation unlike
        # most of you find on the internet)

        # Intervals are:

        # - perfect if: (1) the top note is in the major key of the bottom note AND (2) the
        # - bottom note is in the major key of the top note.
        # - major if the top note is in the major key of the bottom note.
        # - minor if it is a half step smaller than major.
        # - diminished if it is a half step smaller than minor or perfect.
        # - augmented if it is a half step larger than major or perfect.

        # TODO: there should probably be an algorithmic way to do this without using a map that is easily computable

        if semitone_difference > 12:
            semitone_difference %= 12
            staff_position_difference %= 7

        try:

            quality = INTERVAL_QUALITY_MAP[staff_position_difference][semitone_difference]

        except KeyError:
            raise ValueError(f"Cannot find interval quality corresponding to {semitone_difference} semitone "
                             f"difference and {staff_position_difference} staff (scale) position difference")

        return quality

    @classmethod
    def between_notes(cls, note1: Note, note2: Note, scale: Scale):
        """
        Returns an interval between two notes.
        The returned interval has quality info.
        """
        semitone_interval = (note1 - note2).semitones
        staff_interval = scale.all_notes.index(note1) - scale.all_notes.index(note2)

        quality = cls.assess_quality(staff_interval, semitone_interval)
        result = Interval(staff_interval, quality)

        return result

    def is_consonant(self):
        return self in CONSONANT_INTERVALS

    def is_perfect_consonant(self):
        return self in PERFECT_CONSONANT_INTERVALS

    def is_imperfect_consonant(self):
        return self in IMPERFECT_CONSONANT_INTERVALS

    def is_dissonant(self):
        return self in DISSONANT_INTERVALS

    # TODO: inversions


# main (non-compound, less than octave) intervals constants
Interval.P1 = Interval(0, IntervalQuality.PERFECT)
Interval.P8 = Interval(7, IntervalQuality.PERFECT)
Interval.P4 = Interval(3, IntervalQuality.PERFECT)
Interval.P5 = Interval(4, IntervalQuality.PERFECT)

Interval.m2 = Interval(1, IntervalQuality.MINOR)
Interval.m3 = Interval(2, IntervalQuality.MINOR)
Interval.m6 = Interval(5, IntervalQuality.MINOR)
Interval.m7 = Interval(6, IntervalQuality.MINOR)

Interval.M2 = Interval(1, IntervalQuality.MAJOR)
Interval.M3 = Interval(2, IntervalQuality.MAJOR)
Interval.M6 = Interval(5, IntervalQuality.MAJOR)
Interval.M7 = Interval(6, IntervalQuality.MAJOR)

Interval.d5 = Interval(4, IntervalQuality.DIMINISHED)

Interval.A4 = Interval(3, IntervalQuality.AUGMENTED)


# https://music.utk.edu/theorycomp/courses/murphy/documents/Intervals.pdf
PERFECT_CONSONANT_INTERVALS = (
    Interval.P1,   # P1    # TODO: add constants for all these intervals for easier reference?
    Interval.P8,
    Interval.P5,   # P5
    # P4 is weird so it's not added here:
        # The P4 is sometimes consonant and sometimes dissonant.
        # In early music, P4 was a consonance and with other perfect intervals made up
        # most of music compositions.
        # Later, when using complete triads, the 4th tended to lose some of its stability and
        # consonance (sounded like active tone between 5th and 3rd). If it appeared
        # near a 5th (its inversion), then it was stable.
        # SO -- the P4 is a consonant when it functions as an inverted 5th (as part of the
        # chord); otherwise, it is dissonant.
)

IMPERFECT_CONSONANT_INTERVALS = (
    Interval.m3,   # m3
    Interval.M3,   # M3
    Interval.m6,   # m6
    Interval.M6,   # M6
)

CONSONANT_INTERVALS = PERFECT_CONSONANT_INTERVALS + IMPERFECT_CONSONANT_INTERVALS

DISSONANT_INTERVALS = (
    Interval.m2,  # m2
    Interval.M2,  # M2
    Interval.m7,  # m7
    Interval.M7,  # M7
    # tritones
    Interval.d5, # d5 - diminished 5th, tritone
    Interval.A4, # A4 - augmented 4th, tritone
)
