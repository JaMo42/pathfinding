from typing import *
from grid import *
from pathfinder import Pathfinder
from sys import maxsize as INFINITY

NEIGHBORS = (
  (1, -1), (1, 0), (1, 1),
  (0, -1), (0, 1),
  (-1, -1), (-1, 0), (-1, 1)
)


def heuristic(node: Tuple[int, int], end: Tuple[int, int]) -> float:
  D1 = AStar.straight_cost
  D2 = AStar.diagonal_cost
  dx = abs(node[0] - end[0])
  dy = abs(node[1] - end[1])
  return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)


class AStar(Pathfinder):
  straight_cost = 1
  diagonal_cost = 1.414

  def __str__(self) -> str:
    return "A*"

  def get_path(self, start: Tuple[int, int], end: Tuple[int, int]
               ) -> Iterator[Tuple[int, int]]:
    # Discovered nodes
    open_set = set([start])
    self.grid.fill_meta({
      "f": INFINITY,  # f-score
      "g": INFINITY,  # g-score
      "prev": None    # previous node
    })
    self.grid[start].meta = {
      "f": 0,
      "g": heuristic(start, end),
      "prev": None
    }
    while open_set:
      current = min(open_set, key=lambda i: self.grid[i].get('f'))
      if current == end:
        self.reconstruct_path(end)
        break
      open_set.remove(current)
      for neighbor in self.neighbors(current):
        gscore = self.gscore(current) + self.cost(current, neighbor)
        if gscore < self.gscore(neighbor):
          self.grid[neighbor].set("prev", current)
          self.grid[neighbor].set('g', gscore)
          self.grid[neighbor].set('f', gscore + heuristic(neighbor, end))
          open_set.add(neighbor)
      yield current

  def reconstruct_path(self, end: Tuple[int, int]) -> None:
    self.path = []
    while end:
      self.path.insert(0, end)
      end = self.grid[end].get("prev")

  def fscore(self, n: Tuple[int, int]) -> float:
    return self.grid[n].get('f')

  def gscore(self, n: Tuple[int, int]) -> float:
    return self.grid[n].get('g')

  def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
    """ Neighboring nodes of a node """
    n = []
    x, y = node
    for nx, ny in NEIGHBORS:
      Nx = x + nx
      Ny = y + ny
      if Nx >= 0 and Nx < self.grid.width and\
         Ny >= 0 and Ny < self.grid.height:
        n.append((Nx, Ny))
    return [i for i in n if self.grid[i].value == 0]

  def cost(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """ Cost between two nodes """
    x_diff = a[0] != b[0]
    y_diff = a[1] != b[1]
    return self.diagonal_cost if x_diff and y_diff else self.straight_cost
