# Setup sys.path. A bit ugly but avoids setting up setup.py for now.
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))


import collections
import os
import re
import tempfile


from src.alto_tools import alto_tools


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

def test_walker():
    def create_empty_file(fn):
        open(fn, 'a').close()

    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create some test files
        create_empty_file(os.path.join(tmpdirname, 'test1.xml'))
        create_empty_file(os.path.join(tmpdirname, 'test2.xml'))
        create_empty_file(os.path.join(tmpdirname, 'this-should-not-be-returned'))

        # Create a list of inputs
        inputs = [
                os.path.join(tmpdirname, 'test1.xml'),  # Note that this also is in tmpdirname
                tmpdirname
        ]
        fnfilter = lambda fn: fn.endswith('.xml')
        expected = [
                os.path.join(tmpdirname, 'test1.xml'),
                os.path.join(tmpdirname, 'test1.xml'),  # second instance from tmpdirname
                os.path.join(tmpdirname, 'test2.xml')
                # NOT 'this-should-not-be-returned'
        ]
        assert collections.Counter(alto_tools.walker(inputs, fnfilter)) == collections.Counter(expected)
