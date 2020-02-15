from typing import *
import pygame
from grid import *
from pathfinder import Pathfinder
from args import Args
from pygame.locals import *
from os import name as os_name


class Colors:
  empty = (16, 78, 139)
  wall = (156, 161, 163)
  path = (92, 184, 92)
  visited = (217, 83, 79)
  text = (8, 9, 10)


class Display:
  grid: Grid

  def __init__(self, grid: Grid) -> None:
    """
    :param grid: The grid to display.
    :param resolution: Width and height of a cell in pixels.
    :param fullscreen: Whether to run in fullscreen.
    """
    self.scale = Args.get("scale")
    self.grid = grid
    # Create display
    pygame.init()
    if Args.get("fullscreen"):
      display_size = pygame.display.list_modes()[0]
      res = (0, 0)
      if os_name == "nt":
        from ctypes import windll
        windll.user32.SetProcessDPIAware()
      self.surface = pygame.display.set_mode(
        res, flags=DOUBLEBUF | FULLSCREEN | HWSURFACE
      )
    else:
      self.surface = pygame.display.set_mode(
        (grid.width * self.scale, grid.height * self.scale), pygame.DOUBLEBUF
      )
    pygame.event.set_allowed([QUIT, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
    self.surface.set_alpha(None)

  def draw_grid(self) -> None:
    """ Draws the entire grid """
    self.surface.fill(Colors.empty)
    for y in range(self.grid.height):
      for x in range(self.grid.width):
        if self.grid[(x, y)].value == 1:
          rect = pygame.Rect(
            x * self.scale, y * self.scale, self.scale, self.scale)
          pygame.draw.rect(self.surface, Colors.wall, rect)
    pygame.display.flip()

  def draw_cell(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
    rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
    pygame.display.update(pygame.draw.rect(self.surface, color, rect))

  def draw_indicator(self, x: int, y: int) -> None:
    rect = pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
    pygame.display.update(pygame.draw.ellipse(self.surface, Colors.text, rect))

  def get_coord(self, x: int, y: int):
    """ Convert screen coordinate to cell coordinate """
    return x // self.scale, y // self.scale

  def show(self,
           pathfinder: Pathfinder,
           start: Tuple[int, int],
           end: Tuple[int, int]) -> None:
    """ Show a pathfinding algorithm """
    pygame.display.set_caption(str(pathfinder))
    for v in pathfinder.get_path(start, end):
      self.draw_cell(*v, Colors.visited)
      if pygame.event.peek(QUIT):
        return
    for p in pathfinder.path:
      self.draw_cell(*p, Colors.path)
    self.draw_indicator(*start)
    self.draw_indicator(*end)
