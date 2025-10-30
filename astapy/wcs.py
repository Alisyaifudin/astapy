"""wcs extractor module"""
from pathlib import Path
import os
from typing import Union, Optional
from dataclasses import dataclass


@dataclass
class Card:
    '''Basic card'''
    key: str
    value: Union[str, float, bool]
    comment: Optional[str]


@dataclass
class Comment:
    '''Comment card'''
    value: str


def extract_wcs(parent: Path, delete: bool) -> list[Union[Comment, Card]]:
    '''Utility function to extract wcs header values'''
    path = parent / "temp.ini"
    wcs_path = parent / "temp.wcs"
    wcs = []
    if os.path.exists(wcs_path):
        with open(wcs_path, 'r', encoding='utf-8') as f:
            while True:
                line = f.readline().strip()
                if line.startswith('CTYPE'):
                    card = extract_card(line)
                    if card:
                        wcs.append(card)
                    break
            for line in f.readlines():
                card = extract_card(line.strip())
                if card:
                    wcs.append(card)
    if delete:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(wcs_path):
            os.remove(wcs_path)
    return wcs


def extract_card(line: str):
    """Extract card from line"""
    if line.startswith("COMMENT"):
        contents = line.split("COMMENT")
        if len(contents) != 2:
            return None
        return Comment(contents[1])
    else:
        first = line.split("=")
        if len(first) != 2:
            return None
        key = first[0]
        second = first[1].split("/")
        value = second[0]
        if value.isdigit():
            value = float(value)
        elif value == "T":
            value = True
        elif value == "F":
            value = False
        comment = None
        if len(second) == 2:
            comment = second[1]
        return Card(key=key, value=value, comment=comment)
