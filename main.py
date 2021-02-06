class Color:

    def __init__(self, name: str = "#", priority: int = 0):
        self._name: str = name
        self._priority: int = priority

    @property
    def name(self):
        return self._name

    @property
    def priority(self):
        return self._priority

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if type(other) == str:
            return True if self._name == other else False
        elif type(other) == Color:
            return True if self._name == other.name else False
        else:
            return False


class Cell:
    _COLORS: dict = {}

    def __init__(self, row: int, col: int):
        self._row: int = row
        self._column: int = col
        self._value: int = -1
        self._color: Color = Cell.COLORS()["#"]
        self._permitted_values: list = []
        self._permitted_colors: list = []

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        self._value = val

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, _color: str or Color):
        if type(_color) == str:
            self._color = Cell.COLORS()[_color]
        elif type(_color) == Color:
            self._color = _color

    @property
    def permitted_values(self) -> list:
        return self._permitted_values

    @permitted_values.setter
    def permitted_values(self, lst: list):
        self._permitted_values = lst

    @property
    def permitted_colors(self) -> list:
        return self._permitted_colors

    @permitted_colors.setter
    def permitted_colors(self, lst: list):
        self._permitted_colors = lst

    def has_value(self) -> bool:
        return True if self.value != -1 else False

    def has_color(self) -> bool:
        return True if self.color != "#" else False

    @staticmethod
    def decode(_str: str):
        _color_name: str
        _value: int
        if "*" in _str:
            _value = -1
            _color_name = _str.replace("*", "")
        elif "#" in _str:
            _color_name = "#"
            _value = int(_str.replace("#", ""))
        else:
            _tmp_value: str = ""
            for char in _str:
                if char.isdigit():
                    _tmp_value = _tmp_value + char
                else:
                    break
            _color_name = _str.replace(_tmp_value, "")
            _value = int(_tmp_value)
        return _value, _color_name

    @classmethod
    def COLORS(cls):
        return cls._COLORS

    @classmethod
    def setCOLORS(cls, colors: dict):
        cls._COLORS = colors.copy()

    def assignment_complete(self) -> bool:
        if self.value == -1 or self.color == "#":
            return False
        return True

    def __str__(self) -> str:
        _str_value: str = str(self._value) if self._value != -1 else "*"
        return _str_value + str(self._color)

    def __repr__(self) -> str:
        return self.__str__()


class Table:

    def __init__(self, length: int):
        self._length = length
        self._cells: dict = {}
        for i in range(0, length):
            for j in range(0, length):
                self._cells[(i, j)] = Cell(i, j)

    @property
    def cells(self) -> dict:
        return self._cells

    @property
    def length(self) -> int:
        return self._length

    def cell(self, row: int, column: int) -> Cell:
        return self._cells[(row, column)]

    def assignment_complete(self) -> bool:
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                if not self.cell(_row, _col).assignment_complete():
                    return False
        return True

    def spread_cell_constraints(self, _row: int, _col: int):
        if self.cell(_row, _col).has_value():
            for __row in range(0, self.length):
                if not self.cell(__row, _col).has_value() and _row != __row:
                    self.cell(__row, _col).permitted_values.remove(self.cell(_row, _col).value)
            for __col in range(0, self.length):
                if not self.cell(_row, __col).has_value() and _col != __col:
                    self.cell(_row, __col).permitted_values.remove(self.cell(_row, _col).value)

        if self.cell(_row, _col).has_color():
            if _row - 1 > 0 and not self.cell(_row - 1, _col).has_color():
                self.cell(_row - 1, _col).permitted_colors.remove(self.cell(_row, _col).color.name)
            if _row + 1 < self.length and not self.cell(_row + 1, _col).has_color():
                self.cell(_row + 1, _col).permitted_colors.remove(self.cell(_row, _col).color.name)
            if _col - 1 > 0 and not self.cell(_row, _col - 1).has_color():
                self.cell(_row, _col - 1).permitted_colors.remove(self.cell(_row, _col).color.name)
            if _col + 1 < self.length and not self.cell(_row, _col + 1).has_color():
                self.cell(_row, _col + 1).permitted_colors.remove(self.cell(_row, _col).color.name)

    def set_constraints(self) -> bool:
        #   initializing permitted colors and values to default
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                self.cell(_row, _col).permitted_values = list(range(1, self.length + 1))
                self.cell(_row, _col).permitted_colors = list(Cell.COLORS())
        #   spreading constraints
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                self.spread_cell_constraints(_row, _col)
        #   checking if there's empty domain
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                if (not self.cell(_row, _col).has_value()) and len(self.cell(_row, _col).permitted_values) == 0:
                    return False
                if (not self.cell(_row, _col).has_color()) and len(self.cell(_row, _col).permitted_colors) == 0:
                    return False
        return True

    def __str__(self) -> str:
        _s: str = ""
        for _row in range(0, self._length):
            for _col in range(0, self._length):
                _s += str(self.cell(_row, _col)) + "\t"
            _s += "\n"
        return _s

    def copy(self):
        new_table = Table(self.length)
        for i in range(0, self.length):
            for j in range(0, self.length):
                new_table.cell(i, j).value = self.cell(i, j).value
                new_table.cell(i, j).color = self.cell(i, j).color
        return new_table


class Assignment:

    def __init__(self, _type: str, _value: str or int, _row: int, _col: int):
        self._type: str = _type
        self._value: str or int = _value
        self._row = _row
        self._col = _col

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> str or int:
        return self.value

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col


class Node:

    def __init__(self, parent_table: Table, assignment: Assignment):
        self._table: Table = parent_table.copy()
        if assignment.type == "value":
            self._table.cell(assignment.row, assignment.col).value = assignment.value
        elif assignment.type == "color":
            self._table.cell(assignment.row, assignment.col).color = assignment.value

    @property
    def table(self):
        return self._table

    def inference(self) -> bool:
        return self._table.set_constraints()

    def assignment_complete(self) -> bool:
        return self._table.assignment_complete()

    def __str__(self):
        return str(self._table)


class Graph:

    def __init__(self):
        self._visited = []

    def is_visited(self, node: Node) -> bool:
        return True if str(node) in self._visited else False

    def visit(self, node: Node) -> None:
        self._visited.append(str(node))


def main():
    [m, n] = [int(i) for i in input().split()]
    _colors_names = input().split()
    colors: dict = {}
    for color in _colors_names:
        colors[color] = Color(color, _colors_names.index(color) + 1)
    colors["#"] = Color()
    Cell.setCOLORS(colors)
    table = Table(n)
    for _row in range(0, n):
        _row_values = [Cell.decode(code) for code in input().split()]
        for _col in range(0, n):
            _value, _color_name = _row_values[_col]
            table.cell(_row, _col).value = _value
            table.cell(_row, _col).color = _color_name
    print(table)


if __name__ == '__main__':
    main()
    # Cell.setCOLORS({
    #     "#": Color("#", 0),
    #     "a": Color("a", 0),
    #     "b": Color("b", 0),
    # })
    # cell = Cell(1, 4)
    # cell.permitted_colors = list(Cell.COLORS())
    # cell.permitted_colors.remove("a")
    # print(cell.permitted_colors)
