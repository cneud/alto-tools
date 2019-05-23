# Setup sys.path. A bit ugly but avoids setting up setup.py for now.
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))


import os
import re


import alto_tools


datadir = os.path.join(str(Path(__file__).resolve().parent), 'data')


def test_alto_parse():
    f = open(os.path.join(datadir, 'PPN720183197-PHYS_0004.xml'), 'r', encoding='UTF8')
    _, xml, xmlns = alto_tools.alto_parse(f)
    assert xmlns == 'http://www.loc.gov/standards/alto/ns-v3#'


def test_alto_text(capsys):
    f = open(os.path.join(datadir, 'PPN720183197-PHYS_0004.xml'), 'r', encoding='UTF8')
    _, xml, xmlns = alto_tools.alto_parse(f)

    alto_tools.alto_text(xml, xmlns)
    captured = capsys.readouterr()
    assert re.search (r'„Bunte Blätter“', captured.out)
    assert re.search (r'Stille Gedanken', captured.out)
