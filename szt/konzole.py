# coding: utf-8

import sys
import time

from rich.console import Console

from . import barvy

RYCHLE = '-R' in sys.argv[1:]
DÉLKA_PRODLEVY = 0.015

konzole = Console(theme=barvy.barevný_motiv)


def vypiš_barevně(*args, barva=None, **kwargs):
    konzole.print(*args, style=barva, highlight=False, **kwargs)
    if not RYCHLE:
        time.sleep(DÉLKA_PRODLEVY)
