"""Astapy module"""
from typing import Optional, TypedDict
from dataclasses import dataclass, field
from pathlib import Path
from .stream import stream_cmd
from .angle import Angle
from .wcs import extract_wcs


class Config(TypedDict):
    """Configuration"""
    exe: str


_config: Config = {
    'exe': 'astap'
}


def config(c: Config):
    """Update configuration"""
    for key, val in c.items():
        _config[key] = val


class Args(TypedDict, total=False):
    """Additonal args"""
    z: Optional[int]


class AstapNotFound(Exception):
    """Astap executable not found"""

    def __init__(self):
        super().__init__("Astap executable not found")


@dataclass
class Astapy:
    """Astapy class wrapper"""
    file: Path
    r: Angle = field(default_factory=lambda: Angle.from_deg(d=10))
    ra: Angle = field(default_factory=Angle)
    dec: Angle = field(default_factory=Angle)
    fov: Angle = field(default_factory=lambda: Angle.from_deg(d=1))
    _args = {}

    def args(self, **kwargs):
        """Add additional arguments"""
        self._args = kwargs
        return self

    def run(self, log=False, delete=True):
        """Run the alignment algorithm
        Parameters:
          log (bool): show log
          delete (bool): delete the created `temp` file
        """
        f = self.file.absolute().as_posix()
        o: Path = self.file.parent / 'temp'
        cmd = [
            _config["exe"],
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
        try:
            stream_cmd(cmd, log)
        except FileNotFoundError as e:
            if e.filename == _config['exe']:
                raise AstapNotFound from e
            raise
        wcs = extract_wcs(self.file.parent, delete)
        return wcs
