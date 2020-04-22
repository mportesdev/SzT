# coding: utf-8

import sys

from rich.style import Style
from rich.theme import Theme

SVĚTLÉ_BARVY = Theme(
    {
        'červená': Style.parse('bright_red'),
        'modrá': Style.parse('bright_blue'),
        'fialová': Style.parse('bright_magenta'),
        'tyrkys': Style.parse('bright_cyan'),
    }
)
SVĚTLÉ_BARVY_TUČNĚ = Theme(
    {
        'červená': Style.parse('bold bright_red'),
        'modrá': Style.parse('bold bright_blue'),
        'fialová': Style.parse('bold bright_magenta'),
        'tyrkys': Style.parse('bold bright_cyan'),
    }
)
TMAVÉ_BARVY = Theme(
    {
        'červená': Style.parse('red'),
        'modrá': Style.parse('blue'),
        'fialová': Style.parse('magenta'),
        'tyrkys': Style.parse('cyan'),
    }
)
ŽÁDNÉ_BARVY = Theme(
    {
        'červená': Style(),
        'modrá': Style(),
        'fialová': Style(),
        'tyrkys': Style(),
    }
)

if '-B' in sys.argv[1:]:
    barevný_motiv = ŽÁDNÉ_BARVY
elif '-T' in sys.argv[1:]:
    barevný_motiv = TMAVÉ_BARVY
elif sys.platform == 'win32':
    barevný_motiv = SVĚTLÉ_BARVY_TUČNĚ
else:
    barevný_motiv = SVĚTLÉ_BARVY
