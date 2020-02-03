from typing import *
import argparse
from pathfinders import algorithms


class Args:
  args: Dict[str, Any]

  @staticmethod
  def parse() -> None:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--help", action="help")
    p.add_argument(
      "-a", "--algorithm",
      choices=list(algorithms.keys()), default="astar",
      help="The pathfinding algorithm to use"
    )
    p.add_argument(
      "-w", "--width",
      help="The width, in number of cells",
      type=int, default=80
    )
    p.add_argument(
      "-h", "--height",
      help="The height, in number of cells",
      type=int, default=45
    )
    p.add_argument(
      "-s", "--scale",
      help="Width and height of the cells, in pixels",
      type=int, default=20
    )
    Args.args = vars(p.parse_args())

  @staticmethod
  def get(key: str) -> Any:
    return Args.args[key]
