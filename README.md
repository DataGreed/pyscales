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