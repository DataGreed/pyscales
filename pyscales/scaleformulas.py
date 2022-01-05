from pyscales.scales import ScaleFormula


MAJOR_FORMULA = ScaleFormula("wwhwwwh", name="Major (Ionian)")
MINOR_FORMULA = ScaleFormula("whwwhww", name="Natural Minor")
NATURAL_MINOR_FORMULA = MINOR_FORMULA

# modern modes

IONIAN_FORMULA = MAJOR_FORMULA
DORIAN_FORMULA = ScaleFormula("whwwwhw", name="Dorian")
PHRYGIAN_FORMULA = ScaleFormula("hwwwhww", name="Phrygian")
LYDIAN_FORMULA = ScaleFormula("wwwhwwh", name="Lydian")
MIXOLYDIAN_FORMULA = ScaleFormula("wwhwwhw", name="Mixolydian")
Aeolian = MINOR_FORMULA
LOCRIAN_FORMULA = ScaleFormula("hwwhwww", name="Locrian")

