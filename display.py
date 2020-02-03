from typing import *
import pygame
from grid import *
from pathfinder import Pathfinder


class Colors:
  empty = (16, 78, 139)
  wall = (156, 161, 163)
  path = (92, 184, 92)
  visited = (217, 83, 79)
  start_end = (8, 9, 10)


class Display:
  grid: Grid
  start: Optional[Tuple[int, int]]
  end: Optional[Tuple[int, int]]

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

  def render(self) -> None:
    """ Clears the background, draws walls """
    self.surface.fill(Colors.empty)
    for y in range(self.grid.height):
      for x in range(self.grid.width):
        if self.grid[(x, y)].value == 1:
          rect = pygame.Rect(
            x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
          pygame.draw.rect(self.surface, Colors.wall, rect)

  def draw_start_end(self) -> None:
    """ Draw the start and end nodes, if defined """
    def do_draw(x, y):
      rect = pygame.Rect(
        x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
      pygame.draw.ellipse(self.surface, Colors.start_end, rect)
    if self.start is not None:
      do_draw(*self.start)
    if self.end is not None:
      do_draw(*self.end)

  def draw_cell(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
    """ Color a single cell """
    rect = pygame.Rect(
      x * self.cell_x, y * self.cell_y, self.cell_x, self.cell_y)
    pygame.draw.rect(self.surface, color, rect)

  def update(self, render: bool = True, indicators: bool = True):
    """ Render, draw indicators and flip the display """
    if render:
      self.render()
      self.draw_start_end()
    pygame.display.flip()

  def get_coord(self, x: int, y: int):
    """ Convert screen coordinate to cell coordinate """
    return x // self.cell_x, y // self.cell_y

  def show(self,
           pathfinder: Pathfinder,
           start: Tuple[int, int],
           end: Tuple[int, int]) -> None:
    """ Show a pathfinding algorithm """
    pygame.display.set_caption(str(pathfinder))
    self.update()
    update = True
    for v in pathfinder.get_path(start, end):
      # Draw the visited cell
      self.draw_cell(*v, Colors.visited)
      if update:
        self.update(False)
      # Stop if the window should be closed
      if pygame.event.peek(pygame.QUIT):
        return
      # Stop rendering while a mouse button is pressed
      elif pygame.event.peek(pygame.MOUSEBUTTONDOWN):
        update = False
      elif pygame.event.peek(pygame.MOUSEBUTTONUP):
        update = True
    # Draw the path
    for p in pathfinder.path:
      self.draw_cell(*p, Colors.path)
    self.draw_start_end()
    self.update(False)
