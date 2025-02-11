import os
import sys
import tempfile
from typing import Iterable, List

import pytest

from alto_tools import alto_tools


def argv(args: str) -> List[str]:
    """
    >>> argv('-c file')
    ['alto-tools', '-c', 'file']
    """
    return ["alto-tools"] + args.split()


@pytest.fixture
def latin1_input_file_path() -> Iterable[str]:
    with open("tests/data/PPN720183197-PHYS_0004.xml") as f:
        xml = f.read()
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = os.path.join(tmpdir, "iso8859.xml")
        with open(fn, "w+", encoding="iso-8859-1", errors="replace") as f:
            f.write(xml)
        yield fn


def test_single_file_xml_encoding(
    latin1_input_file_path: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fn = latin1_input_file_path
    sys.argv = argv(f"-t -x iso8859-1 {fn}")
    alto_tools.main()
    assert "Stille Gedanken" in capsys.readouterr().out


def test_single_file_file_encoding(
    latin1_input_file_path: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fn = latin1_input_file_path
    sys.argv = argv(f"-t -e iso8859-1 {fn}")
    alto_tools.main()
    assert "Stille Gedanken" in capsys.readouterr().out
