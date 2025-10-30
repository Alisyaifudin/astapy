# ASTApy

Thin wrapper around ASTAP CLI

download astap cli and some database stars.
here https://www.hnsky.org/astap.htm#astap_command_line

# Installation

## ASTAP

Go here: https://www.hnsky.org/astap.htm

Download the cli for your os.

Save the binary in nice location, ex. create this `~/.local/astap`

Save this location in PATH: `export $PATH=~/.local/astap:$PATH`

Rename the cli executatble to `astap`

### Database

download start database, say `D50`. Unpack it, store the data in the same dir for astap cli executable.

### Test CLI

type `astap --help`, it will show the help page.

## ASTApy

Install `Astapy` from PyPi: https://pypi.org/project/astapy/

#### Note

It would be better to install it in `venv`.

# Use

Example usecase

```python
from pathlib import Path
from astapy import Astapy, Angle
# the fits file location. Define the file path using Path from pathlib
file = Path("./data/test.fit")
# define initial coordinate for searching, optional, default to ra=0, dec=0
dec = Angle.from_deg(d=29, m=39, s=49)
ra = Angle.from_hour(h=6, m=30, s=49)

# fielv of fiev of the image, must be close to make the algorithm effective
fov = Angle.from_deg(d=0.18)

# search radius
r = Angle.from_deg(d=10)

# initial Astapy
a = Astapy(file=file, dec=dec, ra=ra, fov=fov, r=r).args(z=1)

# run it and show log
wcs = a.run(log=True)

# print the wcs header value
for val in wcs:
    print(val)
```

### astap cli location

if your `astap` has different name or location, you can configure it. Call this function at the top level.

Let's say your astap cli executable is `astap_cli`


```python
from astapy import config

config({
  'exe': 'astap_cli'
})
```

## Docs

