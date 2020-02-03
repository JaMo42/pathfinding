#!/usr/bin/env python3
import sys
from grid import Grid
from pathfinders import *
from display import Display
import pygame
from args import Args


if __name__ == "__main__":
  Args.parse()

  grid = Grid(Args.get("width"), Args.get("height"))
  pathfinder: Pathfinder = algorithms[Args.get("algorithm")](grid)

  display = Display(grid, (Args.get("scale"), Args.get("scale")))
  quit_flag = False
  clock = pygame.time.Clock()

  start = (0, 0)
  end = (Args.get("width") - 1, Args.get("height") - 1)
  display.start = start
  display.end = end

  painting = False
  painting_what = 0
  thick_brush = True

  display.update()
  while(not quit_flag):
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        quit_flag = True
        break
      elif e.type == pygame.KEYUP:
        if e.key == pygame.K_s:
          start = display.get_coord(*pygame.mouse.get_pos())
          display.start = start
          display.update()
        if e.key == pygame.K_e:
          end = display.get_coord(*pygame.mouse.get_pos())
          display.end = end
          display.update()
        if e.key == pygame.K_r:
          display.show(pathfinder, start, end)
        elif e.key == pygame.K_t:
          thick_brush = not thick_brush
        elif e.key == pygame.K_c:
          grid.fill(0)
          display.update()
      elif e.type == pygame.MOUSEBUTTONDOWN:
        painting = True
        painting_what = 1 if e.button == 1 else 0
      elif e.type == pygame.MOUSEBUTTONUP:
        painting = False
    if painting:
      pos = display.get_coord(*pygame.mouse.get_pos())
      grid[pos].value = painting_what
      if thick_brush and\
          pos[0] >= 1 and pos[0] < (grid.width - 1) and\
          pos[1] >= 1 and pos[1] < (grid.height - 1):
        for i in ((pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                  (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)):
          grid[i].value = painting_what
      display.update()
