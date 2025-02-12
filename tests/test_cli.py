import os
import sys
import tempfile
from typing import Iterable, List

import pytest

from alto_tools import alto_tools

from test_alto_tools import create_empty_file, datadir


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


def test_nonexistant_file_input(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("i/dont/exist.xml -t")
    alto_tools.main()
    assert not capsys.readouterr().out


def test_invalid_input_file(capsys: pytest.CaptureFixture[str]) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        create_empty_file(os.path.join(tmpdir, "empty.xml"))
        sys.argv = argv(f"{tmpdir}/empty.xml -t")
        with pytest.raises(UnboundLocalError):
            alto_tools.main()


def test_single_file_confidence(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("tests/data/PPN750717092-00000780.ocr.xml -c")
    alto_tools.main()
    assert "Confidence: 78.29" in capsys.readouterr().out


def test_multi_files_confidence(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("-c tests/")
    alto_tools.main()
    stdout = capsys.readouterr().out
    assert "Confidence: 78.29" in stdout
    assert "Confidence of folder: " in stdout


def test_single_file_stats(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("-s tests/data/PPN750717092-00000780.ocr.xml")
    alto_tools.main()
    assert "# of <TextLine> elements: 60" in capsys.readouterr().out


def test_single_file_text_extraction(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("-t tests/data/PPN750717092-00000780.ocr.xml")
    alto_tools.main()
    assert (
        "Thüren, Lieferung der erforderlichen Gerüste und"
    ) in capsys.readouterr().out


def test_single_file_illustration_coords(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("-i tests/data/PPN720183197-PHYS_0004.xml")
    alto_tools.main()
    assert "Illustration: block_20=201,321,61,226" in capsys.readouterr().out


def test_single_file_graphic_coords(capsys: pytest.CaptureFixture[str]) -> None:
    sys.argv = argv("-g tests/data/PPN750717092-00000780.ocr.xml")
    alto_tools.main()
    assert "GraphicalElement: Page1_Block29=11,899,2983,549" in capsys.readouterr().out


def test_pipe_input_xml(capsys: pytest.CaptureFixture[str]) -> None:
    with open(os.path.join(datadir, "PPN720183197-PHYS_0004.xml")) as f:
        sys.stdin = f
        sys.argv = ["alto-tools", "-t", "-"]
        alto_tools.main()
    captured = capsys.readouterr()
    assert "Stille Gedanken" in captured.out
