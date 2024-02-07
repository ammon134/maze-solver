from graphics import Point, Line, Window
from typing import Self


class Cell:
    def __init__(self, p1: Point, p2: Point, win: Window):
        self.__p1: Point = p1
        self.__p2: Point = p2
        self.__left: float = min(self.__p1.x, self.__p2.x)
        self.__right: float = max(self.__p1.x, self.__p2.x)
        self.__top: float = max(self.__p1.y, self.__p2.y)
        self.__bottom: float = min(self.__p1.y, self.__p2.y)
        self.has_left = True
        self.has_right = True
        self.has_top = True
        self.has_bottom = True
        self.__win = win

    def get_left_wall(self) -> Line:
        return Line(Point(self.__left, self.__top), Point(self.__left, self.__bottom))

    def get_right_wall(self) -> Line:
        return Line(Point(self.__right, self.__top), Point(self.__right, self.__bottom))

    def get_top_wall(self) -> Line:
        return Line(Point(self.__left, self.__top), Point(self.__right, self.__top))

    def get_bottom_wall(self) -> Line:
        return Line(
            Point(self.__left, self.__bottom), Point(self.__right, self.__bottom)
        )

    def get_center(self) -> Point:
        return Point((self.__left + self.__right) / 2, (self.__top + self.__bottom) / 2)

    def draw(self, fill_color: str):
        if self.has_left:
            self.__win.draw_line(self.get_left_wall(), fill_color)

        if self.has_top:
            self.__win.draw_line(self.get_top_wall(), fill_color)

        if self.has_right:
            self.__win.draw_line(self.get_right_wall(), fill_color)

        if self.has_bottom:
            self.__win.draw_line(self.get_bottom_wall(), fill_color)

    def draw_move(self, cell_to: Self, undo=False):
        self_center = self.get_center()
        cell_to_center = cell_to.get_center()
        if undo:
            fill_color = "red"
        else:
            fill_color = "grey"
        self.__win.draw_line(Line(self_center, cell_to_center), fill_color)
