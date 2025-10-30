# ASTApy

Thin wrapper around ASTAP CLI for Python

Download ASTAP CLI and star database from: https://www.hnsky.org/astap.htm#astap_command_line

## Installation

### ASTAP CLI

1. Go to: https://www.hnsky.org/astap.htm
2. Download the CLI for your operating system
3. Save the binary in a suitable location, for example: `~/.local/astap`
4. Add this location to PATH: `export PATH=~/.local/astap:$PATH`
5. Rename the CLI executable to `astap`

### Star Database

Download a star database (e.g., `D50`), unpack it, and store the data in the same directory as the ASTAP CLI executable.

### Testing the CLI

Type `astap --help` to verify installation. It should display the help page.

### ASTApy Python Package

Install ASTApy from PyPI: https://pypi.org/project/astapy/

```bash
pip install astapy
```

**Note:** It is recommended to install in a virtual environment.

## Usage

Basic example:

```python
from pathlib import Path
from astapy import Astapy, Angle

# Define the FITS file path
file = Path("./data/test.fit")

# Define initial coordinates for searching (optional, defaults to ra=0, dec=0)
dec = Angle.from_deg(d=29, m=39, s=49)
ra = Angle.from_hour(h=6, m=30, s=49)

# Field of view of the image (must be close to actual FOV for effective solving)
fov = Angle.from_deg(d=0.18)

# Search radius
r = Angle.from_deg(d=10)

# Initialize Astapy
a = Astapy(file=file, dec=dec, ra=ra, fov=fov, r=r)

# Run plate solving and show log
wcs = a.run(log=True)

# Print the WCS header values
for val in wcs:
    print(val)
```

### Custom ASTAP CLI Location

If your ASTAP executable has a different name or location, configure it at the top level:

```python
from astapy import config

config({
    'exe': 'astap_cli'
})
```

## API Documentation

### Angle

The `Angle` class wraps an angle value stored internally in decimal degrees. It provides class methods to construct angles from degrees/minutes/seconds or hours/minutes/seconds.

#### Constructor

```python
Angle(_v: Optional[float] = 0.0)
```

Initializes an Angle object directly from a degree value.

**Do not use directly.** Instead, use `.from_deg()` or `.from_hour()`.

**Parameters:**

| Name | Type    | Default | Description                     |
| ---- | ------- | ------- | ------------------------------- |
| \_v  | `float` | 0.0     | Internal angle value in degrees |

**Example:**

```python
a = Angle(45)
print(a.to_deg())  # 45.0
```

#### Class Methods

##### `from_deg(d=0.0, m=0.0, s=0.0) -> Angle`

Creates an Angle from degrees, minutes, and seconds.

To create a negative angle, add a negative sign to `d` only.

**Parameters:**

| Name | Type    | Default | Description          |
| ---- | ------- | ------- | -------------------- |
| d    | `float` | 0.0     | Degrees component    |
| m    | `float` | 0.0     | Arcminutes component |
| s    | `float` | 0.0     | Arcseconds component |

**Returns:** An instance of `Angle`

**Example:**

```python
a = Angle.from_deg(10, 30, 0)
print(a.to_deg())  # 10.5
```

##### `from_hour(h=0.0, m=0.0, s=0.0) -> Angle`

Creates an Angle from hours, minutes, and seconds. One hour corresponds to 15 degrees (useful for right ascension).

**Parameters:**

| Name | Type    | Default | Description       |
| ---- | ------- | ------- | ----------------- |
| h    | `float` | 0.0     | Hours component   |
| m    | `float` | 0.0     | Minutes component |
| s    | `float` | 0.0     | Seconds component |

**Returns:** An instance of `Angle`

**Example:**

```python
a = Angle.from_hour(1, 0, 0)
print(a.to_deg())  # 15.0
```

#### Instance Methods

##### `to_deg() -> float`

Returns the internal value in decimal degrees.

**Example:**

```python
a = Angle.from_deg(12, 30, 0)
print(a.to_deg())  # 12.5
```

#### Complete Example

```python
from astapy import Angle

# From degrees/minutes/seconds
a1 = Angle.from_deg(23, 26, 45)
print(a1)  # Angle(23.445833°)

# From hours/minutes/seconds
a2 = Angle.from_hour(2, 0, 0)
print(a2.to_deg())  # 30.0
```

### Astapy

This module wraps the ASTAP command-line tool, allowing you to run it directly from Python.

#### Data Structures

##### `Config`

A `TypedDict` defining configuration fields.

| Key | Type  | Description                          |
| --- | ----- | ------------------------------------ |
| exe | `str` | Path or name of the ASTAP executable |

##### `Args`

Optional ASTAP command-line arguments. See: https://www.hnsky.org/astap.htm#astap_command_line

##### `AstapNotFound`

Custom exception raised when the ASTAP executable is missing.

#### Constructor

```python
Astapy(file: Path, r: Angle = 10°, ra: Angle = 0°, dec: Angle = 0°, fov: Angle = 1°)
```

**Parameters:**

| Name | Type    | Default | Description                              |
| ---- | ------- | ------- | ---------------------------------------- |
| file | `Path`  | -       | Path to the FITS or image file to solve  |
| r    | `Angle` | 10°     | Search radius around starting coordinate |
| ra   | `Angle` | 0°      | Right ascension initial guess            |
| dec  | `Angle` | 0°      | Declination initial guess                |
| fov  | `Angle` | 1°      | Field of view                            |

**Example:**

```python
from pathlib import Path
from astapy import Astapy, Angle

solver = Astapy(
    Path("example.fits"),
    ra=Angle.from_hour(h=5),
    dec=Angle.from_deg(d=-10)
)
```

#### Methods

##### `args(**kwargs) -> Astapy`

Add additional ASTAP command-line arguments dynamically.

**Parameters:**

| Name       | Type | Description                                   |
| ---------- | ---- | --------------------------------------------- |
| \*\*kwargs | Any  | Command-line options without the leading dash |

Supported args:

| key      | type               | description                                                                                                                                                                                                                      |
| -------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| z        | `int`              | Down sample (binning) of the input image prior to solving. Specify "0" for auto selection..                                                                                                                                      |
| s        | `int`              | Limits the number of star used for the solution. Typical value 500.                                                                                                                                                              |
| t        | `float`            | Tolerance used to compare quads. Typical value 0.007.                                                                                                                                                                            |
| m        | `float`            | This setting could be used to filter out hot pixels.                                                                                                                                                                             |
| check    | `bool`             | Apply a check pattern filter prior to solving. Use for raw OSC images only when binning is set 1x1                                                                                                                               |
| d        | `str`              | Specify a path to the star database                                                                                                                                                                                              |
| D        | `str`              | Specify a star database                                                                                                                                                                                                          |
| sip      | `bool`             | Add SIP ([Simple Image Polynomial](https://www.hnsky.org/astap.htm#sip)) coefficients. Only required to deactivate SIP.                                                                                                          |
| speed    | `'slow' \| 'auto'` | "slow" is forcing more area overlap while searching to improve detection.                                                                                                                                                        |
| update   | `bool`             | Add the solution to the input fits/tiff file header. In case the input is a jpeg, png a new fits will be created.                                                                                                                |
| log      | `bool`             | Write solver log to a .log text file.                                                                                                                                                                                            |
| analyse  | `float`            | Analyse only and report HFD. Windows: errorlevel is the median HFD \* 100M + number of stars used. So the HFD is trunc(errorlevel/1M)/100. For Linux and macOS the info is send to stdout only.                                  |
| extract  | `float`            | As analyse option but additionally export info of all detectable stars to a .csv file. The decimal separator is always a dot.                                                                                                    |
| extract2 | `float`            | Solve image and export info of all detectable stars to a .csv file including α, δ of each detection. SIP polynomial will be used for high precision positions. The decimal separator is always a dot. In versions after 2024-2-1 |
| annotate | `bool`             | Produce a deep sky annotated jpeg file with same name as input file extended with \_annotated.                                                                                                                                   |
| sqm      | `float`            | Measure the sky background value in magn/arcsec2 relative to the stars. The pedestal is the mean value of a dark. Also centalt and airmass are written to the header.                                                            |

Not supported: `-o`, `-debug`, `-tofits`, `-focus1`, `-stack`

**Example:**

```python
solver.args(z=3, sigma=4)
```

##### `run(log=False, delete=True) -> list[Card | Comment]`

Run the ASTAP alignment/plate-solving process.

**Parameters:**

| Name   | Type   | Default | Description                                     |
| ------ | ------ | ------- | ----------------------------------------------- |
| log    | `bool` | `False` | If True, print ASTAP output in real time        |
| delete | `bool` | `True`  | Whether to delete temporary files after solving |

**Returns:** WCS information as a list of `Card` or `Comment` objects

**Raises:**

- `AstapNotFound` if the ASTAP executable cannot be found
- `FileNotFoundError` if the image file does not exist

**Example:**

```python
wcs = solver.run(log=True)
print(wcs)
```

#### Complete Example

```python
from pathlib import Path
from astapy import Astapy, Angle

solver = Astapy(Path("image.fits")).args(z=2)
wcs = solver.run(log=True)
```

### Log Output

#### Successful Solve

```
Running: astap -f test.fit -r 10.0 -ra 6.5136111111111115 -spd 119.66361111111111 -fov 0.18 -o temp -z 1 -log
astap -f test.fit -r 10.0 -ra 6.5136111111111115 -spd 119.66361111111111 -fov 0.18 -o temp -z 1 -log
Using star database D50
Database limit for this FOV is 203 stars.
ASTAP solver version CLI-2025.10.11
Search radius: 10.0 degrees,
Start position: 06: 30  49.0, +29d 39  49
Image height: 0.18 degrees
Binning: 1x1
Image dimensions: 1375x1100
Quad tolerance: 0.007
Minimum star size: 1.5"
Speed: normal
116 stars, 88 quads selected in the image. 112 database stars, 85 database quads required for the 0.20d square search window. Step size 0.18d. Oversize 1.10

24 of 24 quads selected matching within 0.007 tolerance.
Solution["] x:=-0.574225*x+ -0.012891*y+ 401.578769,  y:=-0.013370*x+ 0.573890*y+ -306.168946
Solution found: 06: 30  48.2 +29d 39  49
```

#### Failed Solve

```
Running: astap -f test.fit -r 10.0 -ra 0.0 -spd 119.66361111111111 -fov 0.18 -o temp -z 1 -log
astap -f test.fit -r 10.0 -ra 0.0 -spd 119.66361111111111 -fov 0.18 -o temp -z 1 -log
Using star database D50
Database limit for this FOV is 203 stars.
ASTAP solver version CLI-2025.10.11
Search radius: 10.0 degrees,
Start position: 00: 00  00.0, +29d 39  49
Image height: 0.18 degrees
Binning: 1x1
Image dimensions: 1375x1100
Quad tolerance: 0.007
Minimum star size: 1.5"
Speed: normal
116 stars, 88 quads selected in the image. 112 database stars, 85 database quads required for the 0.20d square search window. Step size 0.18d. Oversize 1.10
0d,1d,1d,1d,1d,2d,2d,2d,2d,3d,3d,3d,3d,4d,4d,4d,4d,5d,5d,5d,5d,6d,6d,6d,6d,7d,7d,7d,7d,8d,8d,8d,9d,9d,9d,9d,10d,10d,10d,No solution found!  :(
```

### WCS Header

The result of plate solving is a WCS header in the form of a list of `Card` or `Comment` objects.

#### `Card`

```python
@dataclass
class Card:
    key: str
    value: str | float | bool
    comment: str | None = None
```

Represents a single key-value pair in the WCS header.

**Attributes:**

| Name    | Type                   | Description                                                |
| ------- | ---------------------- | ---------------------------------------------------------- |
| key     | `str`                  | Header keyword (e.g., CTYPE1, CRVAL1)                      |
| value   | `str \| float \| bool` | Parsed header value, automatically converted when possible |
| comment | `str \| None`          | Optional comment following a / separator                   |

#### `Comment`

```python
@dataclass
class Comment:
    value: str
```

Represents a comment line in the header file (lines starting with COMMENT).

**Attributes:**

| Name  | Type  | Description      |
| ----- | ----- | ---------------- |
| value | `str` | The comment text |

#### Example

```python
solver = Astapy(file=file)
wcs = solver.run(log=True)
for val in wcs:
    print(val)
```

**Output:**

```
Card(key='CTYPE1  ', value=" 'RA---TAN'           ", comment=' first parameter RA,    projection TANgential')
Card(key='CTYPE2  ', value=" 'DEC--TAN'           ", comment=' second parameter DEC,  projection TANgential')
Card(key='CUNIT1  ', value=" 'deg     '           ", comment=' Unit of coordinates')
Card(key='CRPIX1  ', value='  6.880000000000E+002 ', comment=' X of reference pixel')
Card(key='CRPIX2  ', value='  5.505000000000E+002 ', comment=' Y of reference pixel')
Card(key='CRVAL1  ', value='  9.770093978531E+001 ', comment=' RA of reference pixel (deg)')
Card(key='CRVAL2  ', value='  2.966372471539E+001 ', comment=' DEC of reference pixel (deg)')
Card(key='CDELT1  ', value='  1.595471921033E-004 ', comment=' X pixel size (deg)')
Card(key='CDELT2  ', value='  1.594572697506E-004 ', comment=' Y pixel size (deg)')
Card(key='CROTA1  ', value=' -1.333831567642E+000 ', comment=' Image twist of X axis        (deg)')
Card(key='CROTA2  ', value=' -1.286801526764E+000 ', comment=' Image twist of Y axis        (deg)')
Card(key='CD1_1   ', value='  1.595039610045E-004 ', comment=' CD matrix to convert (x,y) to (Ra, Dec)')
Card(key='CD1_2   ', value='  3.713883671986E-006 ', comment=' CD matrix to convert (x,y) to (Ra, Dec)')
Card(key='CD2_1   ', value=' -3.580937559609E-006 ', comment=' CD matrix to convert (x,y) to (Ra, Dec)')
Card(key='CD2_2   ', value='  1.594170560590E-004 ', comment=' CD matrix to convert (x,y) to (Ra, Dec)')
Card(key='PLTSOLVD', value='                    T ', comment=' Astrometric solved by ASTAP_CLI v2025.10.11.')
Comment(value=' 7 Solved in 0.1 sec. Offset was 10.1".')
Comment(value=' cmdline:astap -f test.fit -r 1')
Comment(value=' 0.0 -ra 6.5136111111111115 -spd 119.66361111111111 -fov 0.18 -o')
Comment(value=' temp -z 1 -log')
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
