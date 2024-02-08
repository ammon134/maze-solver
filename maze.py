from typing import List

from cell import Cell
from graphics import Point, Window

import time


class Maze:
    def __init__(
        self,
        x0: float,
        y0: float,
        row_count: int,
        col_count: int,
        cell_width: float,
        cell_height: float,
        win: Window = Window(0, 0),
    ):
        self.__x0 = x0
        self.__y0 = y0
        self.__row_count = row_count
        self.__col_count = col_count
        self.__cell_width = cell_width
        self.__cell_height = cell_height
        self.__win = win

        self.cells = self.__create_cells()
        self.__create_entrance_and_exit()

    def __create_cells(self) -> List:
        cells = []
        for i in range(0, self.__row_count):
            row = []
            for j in range(0, self.__col_count):
                p1 = Point(
                    self.__x0 + self.__cell_width * j,
                    self.__y0 + self.__cell_height * i,
                )
                p2 = Point(
                    self.__x0 + self.__cell_width * (j + 1),
                    self.__y0 + self.__cell_height * (i + 1),
                )
                cell = Cell(p1, p2, self.__win)
                cell.draw("black")
                self.__win.redraw()
                time.sleep(0.05)

                row.append(cell)
            cells.append(row)
        return cells

    def __animate(self) -> None:
        self.__win.redraw()
        time.sleep(0.05)

    def __create_entrance_and_exit(self) -> None:
        entrance = self.cells[0][0]
        entrance.has_top = False
        entrance.draw("black")
        self.__animate()

        exit_cell = self.cells[self.__row_count - 1][self.__col_count - 1]
        exit_cell.has_bottom = False
        exit_cell.draw("black")
        self.__animate()
