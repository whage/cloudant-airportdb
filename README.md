Tested with python 3.5.2, should run fine with >=3.x.x.

# Environment
Run `./install_dependencies.sh` in the project's root (this will only install the cloudant
client package using pip).

# Usage
Currently this is a very basic command-line-only program.
To start it, run `python3 main.py <lat> <lon> <radius>` from
the `src` directory with the required arguments `lat`, `lon` and `radius`.

## Example
```
$ python3 main.py -30 -30 15
```

# TODO:
- fix row count
- fix radius / bounding box calculation
- adapt to web server / client architecture
