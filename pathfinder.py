from typing import *
from abc import ABC, abstractmethod
from grid import Grid


class Pathfinder:
  grid: Grid
  path: List[Tuple[int, int]]

  def __init__(self, grid: Grid) -> None:
    self.grid = grid
    self.path = []

  @abstractmethod
  def __str__(self) -> str:
    """ Returns the display name of the algorithm """
    ...

  @abstractmethod
  def get_path(self, start: Tuple[int, int], end: Tuple[int, int]
               ) -> Iterator[Tuple[int, int]]:
    """
    Generator performing the algorithm.
    The visited cell should be yielded and the pathset the the class' path
    variable.
    """
    ...
