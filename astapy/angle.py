"""This is angle module"""
from enum import Enum
from typing import Literal, Optional


class UNIT(Enum):
    """Unit enum"""
    DEG = 0
    HOUR = 1


class Angle:
    '''Angle class wrapper to store angle related value

    Example: `Angle().from_deg(d=1)` 
    '''
    _v: float = 0  # internal value in degree
    unit = UNIT.DEG

    def __init__(self, _v: Optional[float] = 0):
        self._v = 0 if _v is None else _v

    @classmethod
    def from_deg(cls, d: float = 0, m: float = 0, s: float = 0, sign: Literal[-1, 1] = 1):
        """Generate Angle from degree. Positive sign=1, negatif=-1"""
        v = sign * \
            (d + m/60 + s/3600)
        return cls(v)

    @classmethod
    def from_hour(cls, h: float = 0, m: float = 0, s: float = 0):
        """Generate Angle from degree"""
        v = 15 * (h + m/60 + s/3600)
        return cls(v)

    def to_deg(self) -> float:
        '''To degree decimal value'''
        return self._v
