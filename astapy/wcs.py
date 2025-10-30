"""WCS header extractor module."""

from pathlib import Path
from dataclasses import dataclass
from typing import Union, Optional, List


@dataclass
class Card:
    """Basic FITS header card."""
    key: str
    value: Union[str, float, bool]
    comment: Optional[str] = None


@dataclass
class Comment:
    """Comment card."""
    value: str


def extract_wcs(parent: Path, delete: bool = True) -> List[Union[Card, Comment]]:
    """Extract WCS header values from ASTAP output files.

    Parameters
    ----------
    parent : Path
        Directory containing `temp.wcs` and `temp.ini` files.
    delete : bool, optional
        If True, delete temporary files after extraction (default: True).

    Returns
    -------
    list[Union[Card, Comment]]
        List of header entries (cards and comments).
    """
    path_ini = parent / "temp.ini"
    path_wcs = parent / "temp.wcs"
    wcs: List[Union[Card, Comment]] = []

    if path_wcs.exists():
        with path_wcs.open("r", encoding="utf-8") as f:
            # Skip until first CTYPE card
            for line in f:
                line = line.strip()
                if line.startswith("CTYPE"):
                    card = _extract_card(line)
                    if card:
                        wcs.append(card)
                    break

            # Process remaining header lines
            for line in f:
                card = _extract_card(line.strip())
                if card:
                    wcs.append(card)

    if delete:
        for p in (path_ini, path_wcs):
            if p.exists():
                p.unlink()

    return wcs


def _extract_card(line: str) -> Optional[Union[Card, Comment]]:
    """Extract a header card or comment from a single line."""
    if not line:
        return None

    if line.startswith("COMMENT"):
        value = line.removeprefix("COMMENT").strip()
        return Comment(value=value)

    if "=" not in line:
        return None

    key, rest = map(str.strip, line.split("=", 1))
    value_part, *comment_part = map(str.strip, rest.split("/", 1))

    value: Union[str, float, bool]
    if value_part == "T":
        value = True
    elif value_part == "F":
        value = False
    else:
        try:
            value = float(value_part)
        except ValueError:
            value = value_part.strip("'\" ")

    comment = comment_part[0] if comment_part else None

    return Card(key=key, value=value, comment=comment)
