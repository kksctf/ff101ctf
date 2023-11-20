from typing import Tuple
from pyfiglet import Figlet
from sudoku import Sudoku


def generate_challenge_and_answer() -> Tuple[str, str]:
    puzzle = Sudoku(3).difficulty(0.5)
    challenge = ""

    for s_ in puzzle.board:
        for el in s_:
            challenge += str(el).replace("None", "*")
        challenge += "\n"

    solved = ""

    for s_ in puzzle.solve().board:
        for el in s_:
            solved += str(el)
        solved += "\n"

    return challenge, solved


class CTFDict:
    FLAG: str = "ptctf{1_g0t_s0me_sud0ku_t01l3t_p444p3r}"
    WON: str = "CONGRATS COMRAD! "
    WRONG_ANSWER: str = "W R O N G\n"


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# ASCII ART
figlet = Figlet()
ASCII_ART = figlet.renderText("PT CTF")
