#!/usr/bin/env python3
import sys
from grid import Grid
from pathfinders import *
from display import Display, Colors
import pygame
from args import Args



if __name__ == "__main__":
  Args.parse()

  # Adjust width and height if running in fullscreen
  if Args.get("fullscreen"):
    pygame.init()
    width, height = pygame.display.list_modes()[0]
    Args.args["width"] = width // Args.get("scale")
    Args.args["height"] = height // Args.get("scale")

  grid = Grid(Args.get("width"), Args.get("height"))
  pathfinder = algorithms[Args.get("algorithm")](grid)
  display = Display(grid)

  start = (0, 0)
  end = (Args.get("width") - 1, Args.get("height") - 1)

  quit_flag = False
  painting = False
  painting_what = 0
  thick_brush = True
  do_redraw = False

  def redraw():
    display.draw_grid()
    display.draw_indicator(*start)
    display.draw_indicator(*end)

  redraw()
  while(not quit_flag):
    # Handle input
    for e in pygame.event.get():
      # Quit
      if e.type == pygame.QUIT:
        quit_flag = True
        break
      # Key up
      elif e.type == pygame.KEYUP:
        if e.key == pygame.K_s:
          display.draw_cell(*start, Colors.empty)
          start = display.get_coord(*pygame.mouse.get_pos())
          display.draw_indicator(*start)
        if e.key == pygame.K_e:
          display.draw_cell(*end, Colors.empty)
          end = display.get_coord(*pygame.mouse.get_pos())
          display.draw_indicator(*end)
        if e.key == pygame.K_r:
          redraw()
          if not display.show(pathfinder, start, end):
            quit_flag = True
            break
          do_redraw = True
        elif e.key == pygame.K_t:
          thick_brush = not thick_brush
        elif e.key == pygame.K_c:
          grid.fill(0)
          redraw()
        elif e.key == pygame.K_ESCAPE:
          quit_flag = True
          break
      # Mouse
      elif e.type == pygame.MOUSEBUTTONDOWN:
        if do_redraw:
          redraw()
        painting = True
        painting_what = 1 if e.button == 1 else 0
      elif e.type == pygame.MOUSEBUTTONUP:
        painting = False
    # Paint walls
    if painting:
      pos = display.get_coord(*pygame.mouse.get_pos())
      grid[pos].value = painting_what
      display.draw_cell(*pos, Colors.wall if painting_what == 1 else Colors.empty)
      # Apply thick brush
      if thick_brush and\
          pos[0] >= 1 and pos[0] < (grid.width - 1) and\
          pos[1] >= 1 and pos[1] < (grid.height - 1):
        for i in ((pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                  (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)):
          grid[i].value = painting_what
          display.draw_cell(*i, Colors.wall if painting_what == 1 else Colors.empty)
