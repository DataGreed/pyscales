from pyscales import Scale, scaleformulas, devicekeyboards, Note
from pyscales.keys import PianoKeyboard, PianoKey


def tune_to_white_keys(keyboard: PianoKeyboard, scale: Scale, print_result=False):
    """
    Returns number of semitones (positive or negative) the keyboard should
    be tuned so all of the keys in given chord will be on white keys.
    Returns None if could not be found.
    :param keyboard:
    :param scale:
    :param print_result:
    :return:
    """

    tries = 13  # TODO: do both ways - negative and positive

    tune = 0

    found_tune_semitones = None
    next_found_tune_semitones = None

    for sign in [1, -1]:

        for i in range(tries):

            if found_tune_semitones:
                if i>found_tune_semitones:
                    break;  # we already found the lowest shift to use

            keyboard.tune(i*sign)

            found = True

            for key in keyboard.get_keys_for_scale(scale=scale):
                if key.black():
                    found=False
                    break

            if found:
                next_found_tune_semitones = i*sign
                break

        if found_tune_semitones is None:
            found_tune_semitones = next_found_tune_semitones
        else:
            # use the lowest semitone shift possible in either direction
            if (abs(next_found_tune_semitones) < abs(found_tune_semitones)):
                found_tune_semitones = next_found_tune_semitones

    if print_result:
        print(f"{scale.scale_name()} ; Tune semitones: { found_tune_semitones if not None else 'not found'}")
        if found_tune_semitones is not None:

            print(keyboard.render_keys_in_ascii())
            keyboard.tune(semitones=found_tune_semitones)
            print(keyboard.render_note_scale_in_ascii(scale=scale, render_octave_number=False))

        print() #empty line

    return found_tune_semitones


def main():

    formulas = [scaleformulas.MAJOR_FORMULA, scaleformulas.MINOR_FORMULA]
    notes = PianoKey.DEFAULT_NOTES_ORDER_LIST

    # for debugging
    # formulas = [scaleformulas.MINOR_FORMULA]
    # notes = [Note('c')]

    keyboard = devicekeyboards.op1_keyboard

    print(f"Tuning {keyboard.name} to use white keys for different scales:")

    for formula in formulas:

        for note in notes:

            tune_to_white_keys(keyboard=keyboard, scale=Scale(note, formula), print_result=True)

if __name__ == '__main__':

    main()
