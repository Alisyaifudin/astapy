"""Astapy module — Python wrapper for ASTAP (Astrometric Stacking Program)."""

from typing import Literal, Optional, TypedDict, Any
from dataclasses import dataclass, field
from pathlib import Path

from .stream import stream_cmd
from .angle import Angle
from .wcs import extract_wcs


class Config(TypedDict):
    """Configuration for ASTAP executable."""
    exe: str


_config: Config = {"exe": "astap"}


def config(c: Config) -> None:
    """Update global configuration for ASTAP.

    Parameters
    ----------
    c : Config
        Dictionary containing new configuration keys.
    """
    _config.update(c)


ARGS_AUX = ('update', 'log', 'annotate', 'debug')


class Args(TypedDict, total=False):
    """Optional command-line arguments for ASTAP.

    see https://www.hnsky.org/astap.htm#astap_command_line

    not implemented: `-o`, `-debug`, `-tofits`, `-focus1`, `-stack`
    """
    z: Optional[int]
    s: Optional[int]
    t: Optional[float]
    m: Optional[float]
    check: Optional[bool]
    d: Optional[str]
    D: Optional[str]
    sip: Optional[bool]
    speed: Literal['slow', 'auto']
    update: Optional[bool]
    log: Optional[bool]
    analyse: Optional[float]
    extract: Optional[float]
    extract2: Optional[float]
    annotate: Optional[bool]
    sqm: Optional[float]


class AstapNotFound(Exception):
    """Raised when the ASTAP executable cannot be found."""

    def __init__(self) -> None:
        super().__init__("Astap executable not found")


@dataclass
class Astapy:
    """
    High-level Python interface to the ASTAP command-line solver.

    This class wraps an ASTAP executable call, runs the alignment or plate-solving
    process, and extracts the resulting WCS (World Coordinate System) information.

    Attributes
    ----------
    file : Path
        Path to the input image file.
    r : Angle
        Search radius in degrees.
    ra : Angle
        Initial guess of right ascension.
    dec : Angle
        Initial guess of declination.
    fov : Angle
        Field of view in degrees.
    """

    file: Path
    r: Angle = field(default_factory=lambda: Angle.from_deg(10))
    ra: Angle = field(default_factory=Angle)
    dec: Angle = field(default_factory=Angle)
    fov: Angle = field(default_factory=lambda: Angle.from_deg(1))
    _args: Args = field(default_factory=Args)

    def args(self, **kwargs):
        """Add additional command-line arguments.

        Parameters
        ----------
        **kwargs :
            see https://www.hnsky.org/astap.htm#astap_command_line

            not implemented: `-wcw`, `-tofits`, `-focus1`, `-stack`

            z: `int`

            s: `int`

            t: `float`

            m: `float`

            check: `bool`

            d: `str`

            D: `str`

            sip: `bool`

            speed: `'slow' | 'auto'`

            update: `bool`

            log: `bool`

            analyse: `float`

            extract: `float`

            extract2: `float`

            annotate: `bool`

            debug: `bool`

            sqm: `float`

        Returns
        -------
        Astapy
            The current instance, allowing method chaining.
        """
        valid_keys = Args.__annotations__.keys()
        _args = Args()
        for key, val in kwargs.items():
            if key in valid_keys:
                _args[key] = val
        self._args = _args
        return self

    def run(self, log: bool = False, delete: bool = True) -> Any:
        """Run ASTAP alignment or plate-solving algorithm.

        Parameters
        ----------
        log : bool, optional
            If True, stream the command output to stdout (default: False).
        delete : bool, optional
            If True, delete the temporary files created by ASTAP (default: True).

        Returns
        -------
        Any
            The WCS object or metadata returned by `extract_wcs`.

        Raises
        ------
        AstapNotFound
            If the ASTAP executable cannot be found in PATH.
        FileNotFoundError
            If the input file does not exist.
        """
        f = self.file.absolute().as_posix()
        output_file = self.file.parent / "temp"

        cmd = [
            _config["exe"],
            "-f", f,
            "-r", str(self.r.to_deg()),
            "-ra", str(self.ra.to_deg() / 15),
            "-spd", str(90 + self.dec.to_deg()),
            "-fov", str(self.fov.to_deg()),
            "-o", output_file.absolute().as_posix(),
        ]

        for key, val in self._args.items():
            if isinstance(val, bool):
                if key in ARGS_AUX:
                    if val:
                        cmd.append(f"-{key}")
                else:
                    cmd.extend([f"-{key}", "y" if val else "n"])
                continue
            cmd.extend([f"-{key}", str(val)])

        try:
            stream_cmd(cmd, log)
        except FileNotFoundError as e:
            if e.filename == _config["exe"]:
                raise AstapNotFound from e
            raise

        return extract_wcs(self.file.parent, delete)
