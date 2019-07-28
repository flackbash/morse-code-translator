import keyboard
import time
import sys
import argparse


morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---',
         '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-',
         '..-', '...-', '.--', '-..-', '-.--', '--..', '.----', '..---',
         '...--', '....-', '.....', '-....', '--...', '---..', '----.',
         '-----']
alpha = [ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890']
morse_to_alpha = dict(zip(morse, alpha))
alpha_to_morse = dict(zip(alpha, morse))


def text_from_morse(morse):
    """Convert morse code to alphabet.

    Arguments:
    morse -- A string containing '.' for short, '-' for long and ' ' for a new
             char.

    >>> text_from_morse(".. -.-. .... / -- --- .-. ... . ")
    'ICH MORSE'
    >>> text_from_morse(".")
    'E'
    """
    text = ""
    for i, word in enumerate(morse.split("/")):
        for char in word.split(" "):
            if char in morse_to_alpha:
                text += morse_to_alpha[char]
        if i < len(morse.split("/")) - 1:
            text += " "
    return text


def morse_from_text(text):
    """Convert morse code to alphabet.

    Arguments:
    text -- A string.

    >>> morse_from_text("Ich morse")
    '.. -.-. .... / -- --- .-. ... .'
    """
    text = text.upper()
    morse = ""
    for i, char in enumerate(text):
        if char in alpha_to_morse:
            morse += alpha_to_morse[char]
        if char == " ":
            morse += "/"
        if i < len(text) - 1:
            morse += " "
    return morse


def show_morse_table():
    """Print the morse code table.
    """
    for i, ch in enumerate(alpha):
        if i != 0 and i % 6 == 0:
            print()
        if ch == "1":
            print()
        print("\t\t%s %s" % (ch, alpha_to_morse[ch]), end="")
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Print morse code as you send it.")
    parser.add_argument('-s', '--show_table', action='store_true',
                        help="Print morse table for each new line.")
    parser.add_argument('-d', '--dit_length', default=0.2, type=float,
                        help="Time in seconds of smallest unit, the dit '.'. "
                        "A dah '-' is 3 dits long, A pause between symbols is"
                        " one dit, A pause between characters is 3 dits, a "
                        "pause between words is 7 dits.")
    parser.add_argument('-dw', '--delta_word', type=float,
                        help="Time in seconds after which a pause is treated"
                        " as inter-word-pause.")
    parser.add_argument('-dc', '--delta_char', type=float,
                        help="Time in seconds after which a pause is treated"
                        " as inter-character-pause.")
    parser.add_argument('-t', '--text_to_morse', action='store_true',
                        help="Entered text is converted to morse code.")

    args = parser.parse_args()
    verbose = args.verbose
    show_table = args.show_table

    dit_length = args.dit_length
    d_char = args.delta_char if args.delta_char else dit_length * 3
    d_word = args.delta_word if args.delta_word else dit_length * 7

    text_to_morse = args.text_to_morse

    pressed = None
    released = None
    char_pause = False
    morse_code = ""
    enter_pressed = False

    if not text_to_morse:
        print("Use 'ctrl' as on-key.")
        print("Press enter to convert the sended code to text")

        if show_table:
            show_morse_table()

        while True:
            next_symbol = ""

            if keyboard.is_pressed("ctrl") and not pressed:
                pressed = time.time()
                released = None
                char_pause = False
            elif not keyboard.is_pressed("ctrl") and pressed:
                # Print . or - depending on how long the button was pressed
                delta = time.time() - pressed
                if delta < dit_length:
                    next_symbol = "."
                else:
                    next_symbol = "-"
                # Reset times
                pressed = None
                released = time.time()

            if released and time.time() - released > d_word:
                # Print a slash when the button was released for more than
                # <d_word> seconds indicating a new word
                next_symbol = "/ "
                released = None
            elif released and time.time() - released > d_char \
                    and not char_pause:
                # Print a space indicating a new character
                next_symbol = " "
                char_pause = True

            morse_code += next_symbol

            if verbose and next_symbol:
                print(next_symbol, end="")

            if keyboard.is_pressed("enter") and not enter_pressed:
                # Print morse as alphabetical text on enter press
                if verbose:
                    print()
                print(text_from_morse(morse_code))
                print()

                if show_table:
                    show_morse_table()

                morse_code = ""
                enter_pressed = True
                released = None
                pressed = None
            elif not keyboard.is_pressed("enter"):
                enter_pressed = False

            sys.stdout.flush()
    else:
        while True:
            pass
