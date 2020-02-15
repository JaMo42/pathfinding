# pathfinding

Pathfinding algorithm visualization tool.

## Usage

### Options

```
usage: main.py [--help] [-a {astar}] [-w WIDTH] [-h HEIGHT] [-s SCALE]

optional arguments:
  --help
  -a {astar}, --algorithm {astar}
                        The pathfinding algorithm to use
  -w WIDTH, --width WIDTH
                        The width, in number of cell
  -h HEIGHT, --height HEIGHT
                        The height, in number of cell
  -s SCALE, --scale SCALE
                        Width and height of the cells, in pixels
  -f, --fullscreen      Run in fullscreen, width and height arguments are ignored
```

### Requirements

- pygame (`pip install pygame`)

### Controls

- `S` - Set starting position
- `E` - Set target position
- `C` - Clear grid
- `R` - Run
- `T` - Switch between thick and slim brush
- `LMB` - Draw
- `RMB` - Erase
- `ESC` - Quit
- Hold any mouse button while a algorithm is running, to stop rendering
