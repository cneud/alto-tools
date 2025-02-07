import sys

import pytest

from alto_tools import alto_tools


def argv(args: str) -> list[str]:
    """
    >>> argv('-c file')
    ['alto-tools', '-c', 'file']
    """
    return ["alto-tools"] + args.split()


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
