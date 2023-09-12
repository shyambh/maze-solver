import unittest

from maze_solver import Maze


class Tests (unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0,0, num_rows, num_cols, 10, 10)
        cells = m1.get_cells()

        self.assertEqual(
            len(cells[0]),
            num_cols
        )
        self.assertEqual(
            len(cells),
            num_rows
        )
    
    def test_cell_visit_reset(self):

        num_cols = 12
        num_rows = 10
        m1 = Maze(0,0, num_rows, num_cols, 10, 10)
        cells = m1.get_cells()
        
        for row in cells:
            for col in row:
                 self.assertTrue(col.visited is False, 'All the cell visited property should be reset to False')

if __name__ == "__main__":
    unittest.main()
