from typing import *
from grid import *
from pathfinder import Pathfinder
from sys import maxsize as INFINITY
from pathfinders.astar import NEIGHBORS

def length(a: Tuple[int, int], b: Tuple[int, int]) -> float:
  if a[0] != b[0] and a[1] != b[1]:
    return Dijkstra.diagonal_cost
  return Dijkstra.straight_cost


class Dijkstra(Pathfinder):
  straight_cost = 1
  diagonal_cost = 1.414

  def __str__(self) -> str:
    return "Dijkstra's algorithm"

  def get_path(self, start: Tuple[int, int], end: Tuple[int, int]
               ) -> Iterator[Tuple[int, int]]:
    vertices = set([i for i in self.grid])
    self.grid.fill_meta({
      "dist": INFINITY,
      "prev": None
    })
    self.grid[start].set("dist", 0)

    while vertices:
      u = min(vertices, key=lambda v: self.dist(v))
      vertices.remove(u)
      if u == end:
        self.reconstruct_path(end)
        break
      for neighbor in self.neighbors(u, vertices):
        alt = self.dist(u) + length(u, neighbor)
        if alt < self.dist(neighbor):
          self.grid[neighbor].meta = {
            "dist": alt,
            "prev": u
          }
      yield u

  def reconstruct_path(self, end: Tuple[int, int]) -> None:
    self.path = []
    while end is not None:
      self.path.insert(0, end)
      end = self.grid[end].get("prev")

  def dist(self, n: Tuple[int, int]) -> float:
    return self.grid[n].get("dist")

  def neighbors(self, node: Tuple[int, int], vertices: Set[Tuple[int, int]]
                ) -> List[Tuple[int, int]]:
    n = []
    x, y = node
    for nx, ny in NEIGHBORS:
      Nx = x + nx
      Ny = y + ny
      if Nx >= 0 and Nx < self.grid.width and\
         Ny >= 0 and Ny < self.grid.height and\
         (Nx, Ny) in vertices:
        n.append((Nx, Ny))
    return [i for i in n if self.grid[i].value == 0]
