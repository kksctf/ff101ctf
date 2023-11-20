import secrets
from typing import Tuple
from pyfiglet import Figlet
from random_word import RandomWords


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def generate_challenge_and_answer() -> Tuple[str, str]:
    r = RandomWords()

    sentence = " ".join([r.get_random_word() for x in range(4)])
    gamma = secrets.token_bytes(len(sentence))
    xored = byte_xor(bytes(sentence, encoding="utf-8"), gamma)

    challenge = f"""
    BOB_1: {gamma}\n
    BOB_2: {xored}\n
    ALICE: ???\n
    """

    return challenge, sentence


class CTFDict:
    FLAG: str = "ptctf{byt3s_0p3r4t10ns_4r3_s0_cr4zy}"
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
