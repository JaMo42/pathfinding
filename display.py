from typing import *
import pygame
from pygame.locals import *
from grid import *
from pathfinder import Pathfinder


class Colors:
  empty = (16, 78, 139)
  wall = (156, 161, 163)
  path = (92, 184, 92)
  visited = (217, 83, 79)
  start_end = (0, 0, 0)


class Display:
  framerate: int = 30

  def __init__(self, grid: Grid, resolution: Tuple[int, int]) -> None:
    """
    :param grid: The grid to display.
    :param resolution: Width and height of a cell in pixels.
    """
    self.grid = grid
    self.cell_x, self.cell_y = resolution
    self.surface = pygame.display.set_mode(
      (grid.width * self.cell_x, grid.height * self.cell_y)
    )
    self.start = None
    self.end = None
    self.clock = pygame.time.Clock()

  def render(self) -> None:
    self.surface.fill(Colors.empty)
    for y in range(self.grid.height):
      for x in range(self.grid.width):
        if self.grid[(x, y)].value == 1:
          rect = pygame.Rect(
            x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
          pygame.draw.rect(self.surface, Colors.wall, rect)

  def draw_start_end(self) -> None:
    def do_draw(x, y):
      rect = pygame.Rect(
        x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
      pygame.draw.ellipse(self.surface, Colors.start_end, rect)
    if self.start:
      do_draw(*self.start)
    if self.end:
      do_draw(*self.end)

  def draw_cell(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
    rect = pygame.Rect(
      x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
    pygame.draw.rect(self.surface, color, rect)

  def update(self, render: bool = True, indicators: bool = True):
    if render:
      self.render()
      self.draw_start_end()
    pygame.display.flip()

  def get_coord(self, x: int, y: int):
    return x // self.cell_x, y // self.cell_y

  def show(self,
           pathfinder: Pathfinder,
           start: Tuple[int, int],
           end: Tuple[int, int]) -> None:
    self.update()
    update = True
    for v in pathfinder.get_path(start, end):
      self.draw_cell(*v, Colors.visited)
      if update:
        self.update(False)
      if pygame.event.peek(QUIT):
        return
      elif pygame.event.peek(MOUSEBUTTONDOWN):
        update = False
      elif pygame.event.peek(MOUSEBUTTONUP):
        update = True
    for p in pathfinder.path:
      self.draw_cell(*p, Colors.path)
    self.draw_start_end()
    self.update(False)
