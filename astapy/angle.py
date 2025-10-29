from enum import Enum
from dataclasses import dataclass

class UNIT(Enum):
  DEG = 0
  HOUR = 1

class SIGN(Enum): 
  POS = 0
  NEG = 1

@dataclass
class Angle:
  d: int = 0
  m: int = 0
  s: float = 0
  sign: SIGN = SIGN.POS
  unit: UNIT = UNIT.DEG
  def sign(self, sign: UNIT):
    self.sign = sign
    return self
  def to_deg(self) -> float:
    num = self.d + self.m/60 + self.s/3600
    if self.sign == SIGN.NEG:
      num *= -1
    if self.unit == UNIT.HOUR:
      num *= 15
    return num
