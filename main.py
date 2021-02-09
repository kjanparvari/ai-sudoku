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

    @staticmethod
    def set_constraint_from_color(_cell: Cell, _neighbour: Cell):
        if not _neighbour.has_color():
            if _cell.color in _neighbour.permitted_colors:
                _neighbour.permitted_colors.remove(_cell.color)
        else:
            if _cell.has_value() and (not _neighbour.has_value()):
                if _neighbour.color.priority > _cell.color.priority:
                    _neighbour.permitted_values = [i for i in _neighbour.permitted_values if i > _cell.value]
                elif _neighbour.color.priority < _cell.color.priority:
                    _neighbour.permitted_values = [i for i in _neighbour.permitted_values if i < _cell.value]
            elif (not _cell.has_value()) and (not _neighbour.has_value()):
                if _neighbour.color.priority > _cell.color.priority:
                    for n_value in _neighbour.permitted_values:
                        _flag: bool = False
                        for c_value in _cell.permitted_values:
                            if n_value > c_value:
                                _flag = True
                                break
                        if not _flag:
                            if n_value in _neighbour.permitted_values:
                                _neighbour.permitted_values.remove(n_value)
                elif _neighbour.color.priority < _cell.color.priority:
                    for n_value in _neighbour.permitted_values:
                        _flag: bool = False
                        for c_value in _cell.permitted_values:
                            if n_value < c_value:
                                _flag = True
                                break
                        if not _flag:
                            if n_value in _neighbour.permitted_values:
                                _neighbour.permitted_values.remove(n_value)

    @staticmethod
    def set_constraint_from_value(_cell: Cell, _neighbour: Cell):
        if _neighbour.has_value():
            if _cell.has_color() and (not _neighbour.has_color()):
                if _neighbour.value > _cell.value:
                    _neighbour.permitted_colors = [_color for _color in _neighbour.permitted_colors if
                                                   _color.priority > _cell.color.priority]

                elif _neighbour.value < _cell.value:
                    _neighbour.permitted_colors = [_color for _color in _neighbour.permitted_colors if
                                                   _color.priority < _cell.color.priority]
            elif (not _cell.has_color()) and (not _neighbour.has_color()):
                if _neighbour.value > _cell.value:
                    for n_color in _neighbour.permitted_colors:
                        _flag: bool = False
                        for c_color in _cell.permitted_colors:
                            if n_color.priority > c_color.priority:
                                _flag = True
                                break
                        if not _flag:
                            if n_color in _neighbour.permitted_colors:
                                _neighbour.permitted_colors.remove(n_color)
                elif _neighbour.value < _cell.value:
                    for n_color in _neighbour.permitted_colors:
                        _flag: bool = False
                        for c_color in _cell.permitted_colors:
                            if n_color.priority < c_color.priority:
                                _flag = True
                                break
                        if not _flag:
                            if n_color in _neighbour.permitted_colors:
                                _neighbour.permitted_colors.remove(n_color)

    def spread_cell_constraints(self, _row: int, _col: int):
        _cell: Cell = self.cell(_row, _col)
        if _cell.has_value():
            for __row in range(0, self.length):
                if not self.cell(__row, _col).has_value() and _row != __row:
                    if _cell.value in self.cell(__row, _col).permitted_values:
                        self.cell(__row, _col).permitted_values.remove(_cell.value)
            for __col in range(0, self.length):
                if not self.cell(_row, __col).has_value() and _col != __col:
                    if _cell.value in self.cell(_row, __col).permitted_values:
                        self.cell(_row, __col).permitted_values.remove(_cell.value)

        if _cell.has_color():
            if _row - 1 >= 0:
                _neighbour = self.cell(_row - 1, _col)
                self.set_constraint_from_color(_cell, _neighbour)
            if _row + 1 < self.length:
                _neighbour = self.cell(_row + 1, _col)
                self.set_constraint_from_color(_cell, _neighbour)
            if _col - 1 >= 0:
                _neighbour = self.cell(_row, _col - 1)
                self.set_constraint_from_color(_cell, _neighbour)
            if _col + 1 < self.length:
                _neighbour = self.cell(_row, _col + 1)
                self.set_constraint_from_color(_cell, _neighbour)

        if _cell.has_value():
            if _row - 1 >= 0:
                _neighbour = self.cell(_row - 1, _col)
                self.set_constraint_from_value(_cell, _neighbour)
            if _row + 1 < self.length:
                _neighbour = self.cell(_row + 1, _col)
                self.set_constraint_from_value(_cell, _neighbour)
            if _col - 1 >= 0:
                _neighbour = self.cell(_row, _col - 1)
                self.set_constraint_from_value(_cell, _neighbour)
            if _col + 1 < self.length:
                _neighbour = self.cell(_row, _col + 1)
                self.set_constraint_from_value(_cell, _neighbour)

    def set_constraints(self) -> bool:
        #   initializing permitted colors and values to default
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                self.cell(_row, _col).permitted_values = list(range(1, self.length + 1))
                self.cell(_row, _col).permitted_colors = list(Cell.COLORS().values()).copy()
                self.cell(_row, _col).permitted_colors.remove("#")
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

    def print_permitted(self):
        for _row in range(0, self.length):
            for _col in range(0, self.length):
                _cell = self.cell(_row, _col)
                print(f"{_row}, {_col} -> values: {_cell.permitted_values}")
                print(f"{_row}, {_col} -> colors: {_cell.permitted_colors}\n")

    def __str__(self) -> str:
        _s: str = ""
        for _row in range(0, self._length):
            for _col in range(0, self._length):
                _s += str(self.cell(_row, _col)) + "  "
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

    def __init__(self, _type: str, _value: str or int, _row: int, _col: int, mrv: int = 0):
        self._type: str = _type
        self._value: str or int = _value
        self._row = _row
        self._col = _col
        self._mrv = mrv

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> str or int:
        return self._value

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def mrv(self) -> int:
        return self._mrv


class Node:

    def __init__(self, parent_table: Table, assignment: Assignment):
        self._table: Table = parent_table.copy()
        if assignment.type == "value":
            self._table.cell(assignment.row, assignment.col).value = assignment.value
        elif assignment.type == "color":
            self._table.cell(assignment.row, assignment.col).color = assignment.value
        elif assignment.type == "none":
            pass

    @property
    def table(self):
        return self._table

    def inference(self) -> bool:
        return self._table.set_constraints()

    def get_assignments(self) -> list:
        _cell: Cell
        lst: list = []
        new_assignment: Assignment
        for _row in range(0, self.table.length):
            for _col in range(0, self.table.length):
                _cell = self.table.cell(_row, _col)
                if not _cell.has_color():
                    mrv = len(_cell.permitted_colors)
                    import random
                    new_assignment = Assignment("color", random.choice(_cell.permitted_colors), _cell.row, _cell.column,
                                                mrv)
                    lst.append(new_assignment)
                if not _cell.has_value():
                    mrv = len(_cell.permitted_values)
                    import random
                    new_assignment = Assignment("value", random.choice(_cell.permitted_values), _cell.row, _cell.column,
                                                mrv)
                    lst.append(new_assignment)
        #   sort
        for i in range(0, len(lst)):
            for j in range(i, len(lst)):
                if lst[i].mrv > lst[j].mrv:
                    lst[i], lst[j] = lst[j], lst[i]
        return lst

    def print_permitted(self):
        self.table.print_permitted()

    def assignment_complete(self) -> bool:
        return self._table.assignment_complete()

    def __str__(self):
        return str(self._table)


class Graph:

    def __init__(self, root: Node):
        self._visited: list = []
        self.frontier: list = []
        if not root.inference():
            print("failure")
            exit(-1)
        self.frontier.append(root)

    def is_visited(self, node: Node) -> bool:
        return True if str(node) in self._visited else False

    @staticmethod
    def forward_check(node: Node, assignment: Assignment) -> bool:
        return Node(node.table.copy(), assignment).inference()

    def find_solution(self) -> Node or None:
        while True:
            if len(self.frontier) == 0:
                break
            _node: Node = self.frontier.pop()
            # print(_node)
            # _node.print_permitted()
            if self.is_visited(_node):
                continue
            self.visit(_node)
            _assignments = _node.get_assignments()
            for assignment in _assignments:
                if self.forward_check(_node, assignment):
                    _new_node = Node(_node.table.copy(), assignment)
                    _new_node.inference()
                    if _new_node.assignment_complete():
                        return _new_node
                    if not self.is_visited(_new_node):
                        self.frontier.append(_new_node)
        return None

    def visit(self, node: Node) -> None:
        self._visited.append(str(node))


def main():
    [_, n] = [int(i) for i in input().split()]
    _colors_names = input().split()
    colors: dict = {}
    max_priority = len(_colors_names)
    for color in _colors_names:
        colors[color] = Color(color, max_priority - _colors_names.index(color))
    colors["#"] = Color()
    Cell.setCOLORS(colors)
    table = Table(n)
    for _row in range(0, n):
        _row_values = [Cell.decode(code) for code in input().split()]
        for _col in range(0, n):
            _value, _color_name = _row_values[_col]
            table.cell(_row, _col).value = _value
            table.cell(_row, _col).color = _color_name
    root: Node = Node(table, Assignment("none", 0, 0, 0))
    # print(root)
    graph = Graph(root)
    solution: Node = graph.find_solution()
    if solution is None:
        print("failure")
    else:
        print("solution found:")
        print(solution)


def tmp():
    Cell.setCOLORS({
        "#": Color("#", 0),
        "r": Color("r", 5),
        "g": Color("g", 4),
        "b": Color("b", 3),
        "y": Color("y", 2),
        "p": Color("p", 1),
    })
    _table = Table(3)
    _table.cell(0, 0).value = 1
    _table.cell(0, 1).color = "b"
    _table.cell(1, 1).value = 3
    _table.cell(1, 1).color = "r"
    _table.cell(2, 0).color = "g"
    _table.cell(2, 1).value = 1
    root: Node = Node(_table, Assignment("none", 0, 0, 0))
    print(root)
    # root.print_permitted()
    if not root.inference():
        print("fail")
    root.print_permitted()


if __name__ == '__main__':
    main()
    # tmp()

#
