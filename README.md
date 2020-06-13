# pyscales
Python musical scales handling and piano keys transposing


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
```

## Device Keyboards
```
>>> from pyscales import devicekeyboards
>>> x = devicekeyboards.op1_keyboard.copy()
>>> print(x.render_keys_in_ascii());print(x.render_notes_in_ascii())
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 D0  D#0 E0  F0  F#0 G0  G#0 A1  A#1 B1  C1  C#1 D1  D#1 E1  F1  F#1 G1  G#1 A2  A#2 B2  C2  C#2

>>> print(x.render_keys_in_ascii());print(x.render_notes_in_ascii(False))
 □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □   □   ▩   □   ▩   □   ▩   □   □   ▩   □   ▩   □  
 D   D#  E   F   F#  G   G#  A   A#  B   C   C#  D   D#  E   F   F#  G   G#  A   A#  B   C   C# 
```