# pyscales
Python musical scales handling and piano keys transposing

[![tests](https://github.com/DataGreed/pyscales/actions/workflows/python-app.yml/badge.svg)](https://github.com/DataGreed/pyscales/actions/workflows/python-app.yml)

# Quick & Dirty examples

## Notes and semitones

```python
>>> from pyscales.primitives import *

>>> Note("a") + ToneDelta(semitones=3)
<Note C0>

>>> Note("a") + ToneDelta(semitones=2)
<Note B0>

>>> Note("a") + ToneDelta(semitones=2)*2
<Note C#0>

>>> Note("a") == Note("a")
True

>>> Note("a", 1) - Note("a", 2)
<ToneDelta -12>

>>> Note("b") - ToneDelta(semitones=2)
<Note A0>

>>> Note("a") - Note("b")
<ToneDelta -2>

>>> Note("a") + ToneDelta(semitones=2)*2
<Note C#0>

>>> Note("a", 4).frequency # in Hz
440

>>> Note("b", 4).frequency  # in Hz
493.8833012561241
```

## Device Keyboards
```python
>>> from pyscales import devicekeyboards
>>> x = devicekeyboards.op1_keyboard.copy()
>>> print(x.render_keys_in_ascii());print(x.render_notes_in_ascii())
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 F0  F#0 G0  G#0 A0  A#0 B0  C1  C#1 D1  D#1 E1  F1  F#1 G1  G#1 A1  A#1 B1  C2  C#2 D2  D#2 E2 

>>> print(x.render_keys_in_ascii());print(x.render_notes_in_ascii(False))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 F   F#  G   G#  A   A#  B   C   C#  D   D#  E   F   F#  G   G#  A   A#  B   C   C#  D   D#  E  

>>> from pyscales import scaleformulas
>>> from pyscales.primitives import Note
>>> from pyscales.scales import Scale
>>> print(x.render_keys_in_ascii());print(x.render_note_scale_in_ascii(Scale(Note("C"), scaleformulas.MAJOR_FORMULA)))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 F0      G0      A0      B0  C1      D1      E1  F1      G1      A1      B1  C2      D2      E2
 
>>> print(x.render_keys_in_ascii());print(x.render_note_scale_in_ascii(Scale(Note("C"), scaleformulas.MINOR_FORMULA)))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 F0      G0  G#0     A#0     C1      D1  D#1     F1      G1  G#1     A#1     C2      D2  D#2
 
>>>  print(x.render_keys_in_ascii());print(x.render_note_scale_in_ascii(Scale(Note("C"), scaleformulas.MINOR_FORMULA)))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 F0      G0  G#0     A#0     C1      D1  D#1     F1      G1  G#1     A#1     C2      D2  D#2
     
>>> x.tune(semitones = 3)   # raise every key by 3 semitones
>>> print(x.render_keys_in_ascii());print(x.render_note_scale_in_ascii(Scale(Note("C"), scaleformulas.MINOR_FORMULA)))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 G#0     A#1     C0      D0  D#1     F1      G1  G#1     A#2     C1      D1  D#2     F2      G2  
 
```

## TODOs

- modes
- midi note numbers
- init note from midi number
- intervals (are there any scientific notations for intervals?)
- add and subtract intervals within a context of a scale
- chords with scales, chord names and notes they consist of (don't forget octaves and root notes)
- chords in given scales (similar to notes_in_scale method)
- chord transposing by adding or subtracting tonedeltas
- init chord from given notes (check if matches any formula)
- find nearest note to a given frequency
- pip package
- chord progressions suggestor utility (linked list? generator?)
- chord progression generator
- ~~note frequencies~~