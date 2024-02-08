from graphics import Window, Point
from cell import Cell
from maze import Maze


def main():
    win = Window(800, 600)
    x1 = 0
    y1 = 0

    x2 = 265
    y2 = 275
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    cell1 = Cell(p1, p2, win)
    cell1.draw("black")

    cell2 = Cell(Point(x1 + 100, y1 + 100), Point(x2 + 100, y2 + 100), win)
    cell2.has_left = False
    cell2.draw("black")

    cell3 = Cell(Point(x1 + 200, y1 + 200), Point(x2 + 200, y2 + 200), win)
    cell3.has_right = False
    cell3.draw("black")

    cell4 = Cell(Point(x1 + 400, y1 + 400), Point(x2 + 400, y2 + 400), win)
    cell4.has_bottom = False
    cell4.draw("black")

    cell5 = Cell(Point(x1 + 500, y1 + 500), Point(x2 + 500, y2 + 500), win)
    cell5.has_top = False
    cell5.draw("black")

    cell5.draw_move(cell4)
    cell3.draw_move(cell1, undo=True)

    win.wait_for_close()


def main2():
    win = Window(1000, 1000)
    maze = Maze(20, 20, 5, 6, 20, 20, win)
    win.wait_for_close()


main2()
