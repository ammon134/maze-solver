from typing import Dict, List

from cell import Cell
from graphics import Point, Window

import random


class Maze:
    def __init__(
        self,
        x0: float,
        y0: float,
        row_count: int,
        col_count: int,
        cell_width: float,
        cell_height: float,
        win: Window | None = None,
    ):
        self.__x0 = x0
        self.__y0 = y0
        self.__row_count = row_count
        self.__col_count = col_count
        self.__cell_width = cell_width
        self.__cell_height = cell_height
        self.__win = win

        self.__cells = self.__create_cells()
        self.__create_entrance_and_exit()
        self.__break_walls_r(0, 0)

    def __create_cells(self) -> List[List[Cell]]:
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
                self.__animate()

                row.append(cell)
            cells.append(row)
        return cells

    def __animate(self) -> None:
        if not self.__win:
            return

        self.__win.redraw()
        # time.sleep(0.05)

    def get_cells(self) -> List[List[Cell]]:
        return self.__cells

    def __create_entrance_and_exit(self) -> None:
        entrance = self.__cells[0][0]
        entrance.has_top = False
        entrance.draw("black")
        self.__animate()

        exit_cell = self.__cells[self.__row_count - 1][self.__col_count - 1]
        exit_cell.has_bottom = False
        exit_cell.draw("black")
        self.__animate()

    def __break_walls_r(self, i: int, j: int) -> None:

        if not self.__win:
            print("Window not available, not drawing")
            return

        current_cell = self.__cells[i][j]
        current_cell.visited = True

        # directional definitions
        directions = {
            "up": {"x": i - 1, "y": j},
            "down": {"x": i + 1, "y": j},
            "left": {"x": i, "y": j - 1},
            "right": {"x": i, "y": j + 1},
        }

        while True:

            allowed_directions: Dict[str, Dict[str, int]] = {}
            for dir in directions:
                x = directions[dir]["x"]
                y = directions[dir]["y"]
                if (
                    0 <= x < self.__row_count
                    and 0 <= y < self.__col_count
                    and self.__cells[x][y].visited is False
                ):
                    allowed_directions[dir] = directions[dir]

            if len(allowed_directions) == 0:
                return

            # Choose a random direction
            # random.seed(1)
            chosen_direction_name = random.choice(list(allowed_directions.keys()))
            chosen_direction = allowed_directions[chosen_direction_name]

            # Break wall between these two cells
            next_cell = self.__cells[chosen_direction["x"]][chosen_direction["y"]]

            if chosen_direction_name == "left":
                current_cell.has_left = False
                next_cell.has_right = False
            if chosen_direction_name == "up":
                current_cell.has_top = False
                next_cell.has_bottom = False
            if chosen_direction_name == "right":
                current_cell.has_right = False
                next_cell.has_left = False
            if chosen_direction_name == "down":
                current_cell.has_bottom = False
                next_cell.has_top = False

            current_cell.draw("black")
            next_cell.draw("black")
            self.__animate()

            self.__break_walls_r(chosen_direction["x"], chosen_direction["y"])
