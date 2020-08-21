import unittest
import bl.board


class TestBLBoardMethods(unittest.TestCase):

    def row_column_index_check(self, arow, brow, acol, bcol, index_value):
        for i in range(arow, brow):
            for j in range(acol, bcol):
                square_index = bl.board.get_square_index_by_coordinates(i, j)
                self.assertEqual(square_index, index_value)

    def test_get_first_index_by_coordinates(self):
        self.row_column_index_check(arow=1, brow=3, acol=1, bcol=3, index_value=1)

    def test_get_second_index_by_coordinates(self):
        self.row_column_index_check(arow=1, brow=3, acol=4, bcol=6, index_value=2)

    def test_get_third_index_by_coordinates(self):
        self.row_column_index_check(arow=1, brow=3, acol=7, bcol=9, index_value=3)

    def test_get_fourth_index_by_coordinates(self):
        self.row_column_index_check(arow=4, brow=6, acol=1, bcol=3, index_value=4)

    def test_get_fifth_index_by_coordinates(self):
        self.row_column_index_check(arow=4, brow=6, acol=4, bcol=6, index_value=5)

    def test_get_sixth_index_by_coordinates(self):
        self.row_column_index_check(arow=4, brow=6, acol=7, bcol=9, index_value=6)

    def test_get_seventh_index_by_coordinates(self):
        self.row_column_index_check(arow=7, brow=9, acol=1, bcol=3, index_value=7)

    def test_get_eighth_index_by_coordinates(self):
        self.row_column_index_check(arow=7, brow=9, acol=4, bcol=6, index_value=8)

    def test_get_ninth_index_by_coordinates(self):
        self.row_column_index_check(arow=7, brow=9, acol=7, bcol=9, index_value=9)

    def test_raises_invalid_coord(self):
        self.assertRaises(ValueError, bl.board.get_square_index_by_coordinates, 10, 1)
        self.assertRaises(ValueError, bl.board.get_square_index_by_coordinates, 1, None)
        self.assertRaises(ValueError, bl.board.get_cell_index_by_coords, 10, 1)
        self.assertRaises(ValueError, bl.board.get_cell_index_by_coords, 1, None)
        self.assertRaises(ValueError, bl.board.get_cell_index_by_coords, 0, 1)

    def test_cell_index_by_coords(self):
        self.assertEqual(1, bl.board.get_cell_index_by_coords(1, 1))
        self.assertEqual(9, bl.board.get_cell_index_by_coords(1, 9))
        self.assertEqual(10, bl.board.get_cell_index_by_coords(2, 1))
        self.assertEqual(18, bl.board.get_cell_index_by_coords(2, 9))
        self.assertEqual(28, bl.board.get_cell_index_by_coords(4, 1))
        self.assertEqual(81, bl.board.get_cell_index_by_coords(9, 9))


if __name__ == '__main__':
    unittest.main()
