import json


# init full list of available value variants (1-9)
def init_value_variants():
    return [n for n in range(1, 10)]


# validate cell coordinates
def check_coordinates(*args):
    def check_coord(coord):
        if (not coord) or (coord < 1) or (coord > 9):
            raise ValueError(
                f'Invalid coordinate value: {coord}')

    for arg in args:
        check_coord(arg)


# cell index by cell coordinates (1-9)
def get_cell_index_by_coords(row_coord, col_coord):
    check_coordinates(row_coord, col_coord)
    return (row_coord - 1) * 9 + col_coord


# square index by cell coordinates (1-9 from left to right top to down)
def get_square_index_by_coordinates(row_coord, column_coord):
    def get_coeff_by_coordinate(coord):
        if 1 <= coord <= 3:
            square_coeff = 1
        elif 4 <= coord <= 6:
            square_coeff = 2
        elif 7 <= coord <= 9:
            square_coeff = 3

        return square_coeff

    check_coordinates(row_coord, column_coord)
    row_coeff = get_coeff_by_coordinate(row_coord)
    column_coeff = get_coeff_by_coordinate(column_coord)

    if row_coeff == 2 and column_coeff == 1:
        index = 4
    elif row_coeff == 2 and column_coeff == 2:
        index = 5
    elif row_coeff == 3 and column_coeff == 1:
        index = 7
    elif row_coeff == 3 and column_coeff == 2:
        index = 8
    else:
        index = row_coeff * column_coeff
    return index


# a cell of the board
class Cell(object):
    # constructor
    def __init__(self, row_coord, column_coord, value=None, value_variants=None):
        self.row_coord = row_coord
        self.column_coord = column_coord
        self.value = value
        self.value_variants = init_value_variants()

    # recalculate available value variants from outside
    def set_value(self, value):
        if not value:
            self.value = None
        elif value in self.value_variants:
            self.value = value
        else:
            error_txt = "Value '{}' can't be set. Cell attributes: row '{}'; column '{}';  value '{}'".format(value, self.row_coord, self.column_coord, self.value)
            raise ValueError(error_txt)


class CellEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cell):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


# row, column, square
class CellAggregator(object):
    # constructor
    def __init__(self, index):
        self.cells = []
        self.index = index
        self.value_variants = set(init_value_variants())

    def add_cell(self, cell):
        self.cells.append(cell)
        if cell.value:
            self.value_variants.remove(cell.value)

    # recalculate available value variants for cells without value
    def recalculate_value_variants(self, full_recalculation=False):
        if full_recalculation:
            self.value_variants = set(init_value_variants())

        for c in self.cells:
            if c.value and c.value in self.value_variants:
                self.value_variants.remove(c.value)


class Board(object):
    # define square by a cell
    def get_square_by_cell(self, cell):
        # square index (1-9) (from left to right top to down)
        index = get_square_index_by_coordinates(cell.row_coord, cell.column_coord)
        if len(self.squares) < index:
            return CellAggregator(index)
        else:
            return self.squares[index - 1]

    # constructor
    def __init__(self):
        self.cells = []
        self.rows = []
        self.columns = []
        self.squares = []
        for i in range(1, 10):
            # the row of the table
            row = CellAggregator(i)
            self.rows.append(row)

            for j in range(1, 10):
                # the column of the table
                if i == 1:
                    column = CellAggregator(j)
                    self.columns.append(column)

                # the cell of the table
                cell = Cell(i, j)
                self.cells.append(cell)

                # the cell in the row
                row.add_cell(cell)

                # the cell in the column
                column = self.columns[j - 1]
                column.add_cell(cell)

                # the square of the table
                square = self.get_square_by_cell(cell)
                self.squares.append(square)
                # the cell in the square
                square.add_cell(cell)

    # print table on console
    def display(self):
        def compose_cell_print(cell):
            return '|' + (str(cell.value) if cell.value else '') + '|' + ('+' if not cell.column_coord % 3 else '')

        cell_index = 0
        for i in range(9):
            strline = ''
            for j in range(9):
                cell = self.cells[cell_index]
                strline += compose_cell_print(cell)
                cell_index += 1

            print(strline)
            if i % 3 == 2:
                print('+' * 55)

    # recalculate available value variants (cell, row, column, square)
    def recalculate_value_variants(self, cell, full_recalculation = False):
        # row
        row = self.rows[cell.row_coord - 1]
        row.recalculate_value_variants(full_recalculation)
        # column
        column = self.columns[cell.column_coord - 1]
        column.recalculate_value_variants(full_recalculation)
        # square
        square = self.get_square_by_cell(cell)
        square.recalculate_value_variants(full_recalculation)
        if cell.value:
            cell.value_variants = []
        else:
            cell.value_variants = row.value_variants & column.value_variants & square.value_variants

    # set cell value by cell coordinates
    def set_cell_value(self, row_coord, column_coord, value):
        cell_index = get_cell_index_by_coords(row_coord, column_coord)
        cell = self.cells[cell_index - 1]
        cell.set_value(value)
        #  recalculate available value variants (cell, row, column, square)
        self.recalculate_value_variants(cell, True if not value else False)

    # print cell aggregators' value variants on console
    def print_cell_aggregators_value_variants(self, cell):
        row = self.rows[cell.row_coord - 1]
        column = self.columns[cell.column_coord - 1]
        square = self.get_square_by_cell(cell)
        print('row.value_variants:', row.value_variants)
        print('col.value_variants:', column.value_variants)
        print('sqr.value_variants:', square.value_variants)

    def cells_to_json(self):
        with open('cells.json', 'w') as f:
            json.dump(self.cells, f, cls=CellEncoder)

    def cells_from_json(self):
        with open("cells.json", "r") as f:
            json_cells_list = json.load(f)
            for json_cell in json_cells_list:
                self.set_cell_value(json_cell['row_coord'], json_cell['column_coord'], json_cell['value'])
