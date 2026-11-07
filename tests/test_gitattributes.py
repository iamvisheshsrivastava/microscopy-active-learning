from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _gitattributes() -> str:
    return (ROOT / ".gitattributes").read_text(encoding="utf-8")


def test_gitattributes_normalises_text_files_to_lf():
    assert "* text=auto eol=lf" in _gitattributes()


def test_gitattributes_marks_binary_assets():
    attrs = _gitattributes()
    for pattern in ("*.png binary", "*.npz binary", "*.pdf binary"):
        assert pattern in attrs
