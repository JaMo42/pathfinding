from typing import *
from copy import deepcopy


class Node:
  value: int
  meta: dict

  def __init__(self, value: int = 0, meta: dict = {}):
    self.value, self.meta = value, meta

  def get(self, attr: str) -> Any:
    return self.meta[attr]

  def set(self, attr: str, value: Any) -> None:
    self.meta[attr] = value


class Grid:
  nodes: List[Node]
  # Graph is represented is represented as adjacency matrix
  # Dimensions of the matrix
  width: int
  height: int

  def __init__(self, width: int, height: int) -> None:
    self.width, self.height = width, height
    self.nodes = [Node() for i in range(width * height)]

  def set_nodes(self, nodes: List[int]) -> None:
    assert(len(nodes) == self.width * self.height)
    self.nodes = [Node(i) for i in nodes]

  def fill_meta(self, meta: Dict[str, Any]) -> None:
    for i in range(self.width * self.height):
      self.nodes[i].meta = deepcopy(meta)

  def fill(self, value: int) -> None:
    for i in range(self.width * self.height):
      self.nodes[i].value = value

  def __getitem__(self, xy: Tuple[int, int]) -> Node:
    return self.nodes[xy[0] + xy[1] * self.width]

  def __setitem__(self, xy: Tuple[int, int], value: int) -> None:
    self.nodes[xy[0] + xy[1] * self.width].value = value

  def __iter__(self) -> Iterator[Tuple[int, int]]:
    for y in range(self.height):
      for x in range(self.width):
        yield (x, y)
