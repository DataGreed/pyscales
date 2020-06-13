from pyscales.keys import PianoKeyboard

# classic piano with 88 keys
classic_88_key_piano_keyboard = PianoKeyboard(number_of_keys=88, first_key_number=1,
                                              first_octave_number=0, name="Classic 88 Key Piano")

# teenage engineering op-1 keyboard
op1_keyboard = PianoKeyboard(number_of_keys=24, first_key_number=6,
                             first_octave_number=0, name="Teenage Engineering OP-1")

# teenabe engineering op-z keyboard
opz_keyboard = op1_keyboard.copy()
opz_keyboard.name="Teenage Engineering OP-Z"

# korg volca keys synthesizer
korg_volca_keys_keyboard = PianoKeyboard(number_of_keys=27, first_key_number=6,
                                         first_octave_number=0, name="Korg Volca Keys")
