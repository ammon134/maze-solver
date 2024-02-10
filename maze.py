from typing import List

from cell import Cell
from graphics import Point, Window

import random
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
        self.__reset_cells_visited()

    def __create_cells(self) -> List[List[Cell]]:
        cells: List[List[Cell]] = []
        for i in range(0, self.__row_count):
            col: List[Cell] = []
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

                col.append(cell)
            cells.append(col)
        return cells

    def __animate(self) -> None:
        if not self.__win:
            return

        self.__win.redraw()
        time.sleep(0.02)

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

            allowed_directions: List[str] = []
            for dir in directions:
                x = directions[dir]["x"]
                y = directions[dir]["y"]
                if (
                    0 <= x < self.__row_count
                    and 0 <= y < self.__col_count
                    and self.__cells[x][y].visited is False
                ):
                    allowed_directions.append(dir)

            if len(allowed_directions) == 0:
                return

            # Choose a random direction
            # random.seed(1)
            chosen_direction_name = random.choice(allowed_directions)
            chosen_direction = directions[chosen_direction_name]

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

    def __reset_cells_visited(self) -> None:
        for col in self.__cells:
            for cell in col:
                cell.visited = False

    def __solve_r(self, i: int, j: int) -> bool:

        current_cell = self.__cells[i][j]
        current_cell.visited = True

        if i == self.__row_count - 1 and j == self.__col_count - 1:
            return True

        # direction definitions
        directions = {
            "up": {"x": i - 1, "y": j},
            "down": {"x": i + 1, "y": j},
            "left": {"x": i, "y": j - 1},
            "right": {"x": i, "y": j + 1},
        }

        allowed_direction_name: List[str] = []
        if not current_cell.has_left:
            allowed_direction_name.append("left")
        if not current_cell.has_top:
            allowed_direction_name.append("up")
        if not current_cell.has_right:
            allowed_direction_name.append("right")
        if not current_cell.has_bottom:
            allowed_direction_name.append("down")

        for dir in allowed_direction_name:
            x = directions[dir]["x"]
            y = directions[dir]["y"]
            if not (
                0 <= x < self.__row_count
                and 0 <= y < self.__col_count
                and self.__cells[x][y].visited is False
            ):
                allowed_direction_name.remove(dir)

        print(f"allowed_direction_name: {allowed_direction_name}")

        if len(allowed_direction_name) == 0:
            return False

        random.shuffle(allowed_direction_name)
        for dir in allowed_direction_name:
            print(
                f"direction x: {directions[dir]['x']}, direction y: {directions[dir]['y']}"
            )
            cell_to = self.__cells[directions[dir]["x"]][directions[dir]["y"]]
            current_cell.draw_move(cell_to)
            self.__animate()

            result = self.__solve_r(directions[dir]["x"], directions[dir]["y"])
            if result:
                return True
            current_cell.draw_move(cell_to, undo=True)
            self.__animate()
        return False

    def solve(self) -> None:
        self.__solve_r(0, 0)
