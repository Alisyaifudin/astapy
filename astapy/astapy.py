from dataclasses import dataclass, field
from pathlib import Path
from .stream import stream_cmd
from .angle import Angle
from .wcs import extract_wcs

@dataclass
class Astapy:
  file: Path
  r: Angle = field(default_factory=lambda: Angle(d=10))
  ra: Angle = field(default_factory=Angle)
  dec: Angle = field(default_factory=Angle)
  fov: Angle = field(default_factory=lambda: Angle(d=1))
  _args = {}
  def args(self, **kwargs):
    self._args = kwargs
    return self
  def run(self, log = False, delete = True):
    f = self.file.absolute().as_posix()
    o: Path = self.file.parent / 'temp'
    cmd = [
        "astap",
        "-f", f,
        "-r", str(self.r.to_deg()),
        "-ra", str(self.ra.to_deg()/15),
        "-spd", str(90 + self.dec.to_deg()),
        "-fov", str(self.fov.to_deg()),
        "-o", o.absolute().as_posix()
    ]
    for key, val in self._args.items():
      cmd.append("-" + key)
      cmd.append(str(val))
    stream_cmd(cmd, log)
    wcs = extract_wcs(self.file.parent, delete)
    return wcs
