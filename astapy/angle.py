"""Angle module for representing and converting angular measurements."""

from typing import Optional


class Angle:
    """
    A class to represent an angle and provide conversion utilities.

    Examples
    --------
    >>> Angle.from_deg(30).to_deg()
    30.0
    >>> Angle.from_deg(10, 30, 0).to_deg()
    10.5
    >>> Angle.from_hour(1, 0, 0).to_deg()
    15.0
    """

    def __init__(self, degrees: Optional[float] = 0.0) -> None:
        """Initialize an angle object.

        Parameters
        ----------
        degrees : float, optional
            The internal angle value in degrees (default is 0.0).
        """
        self._degrees: float = 0.0 if degrees is None else float(degrees)

    @classmethod
    def from_deg(
        cls,
        d: float = 0.0,
        m: float = 0.0,
        s: float = 0.0,
    ) -> "Angle":
        """Create an Angle instance from degrees, minutes, and seconds.

        Parameters
        ----------
        d : float
            Degrees component.
        m : float
            Arcminutes component.
        s : float
            Arcseconds component.

        To make negative angle, add negative sign to `d` ONLY

        Returns
        -------
        Angle
            A new Angle instance.
        """
        sign = 1.0 if d == 0 else d / abs(d)
        degrees = sign * (d + m / 60 + s / 3600)
        return cls(degrees)

    @classmethod
    def from_hour(cls, h: float = 0.0, m: float = 0.0, s: float = 0.0) -> "Angle":
        """Create an Angle instance from hours, minutes, and seconds.

        One hour corresponds to 15 degrees.

        Parameters
        ----------
        h : float
            Hours component.
        m : float
            Minutes component.
        s : float
            Seconds component.

        Returns
        -------
        Angle
            A new Angle instance.
        """
        degrees = 15 * (h + m / 60 + s / 3600)
        return cls(degrees)

    def to_deg(self) -> float:
        """Return the internal angle value in decimal degrees.

        Returns
        -------
        float
            Angle value in degrees.
        """
        return self._degrees

    def __repr__(self) -> str:
        return f"Angle({self._degrees:.6f}°)"
