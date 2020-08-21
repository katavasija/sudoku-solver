import bl.board

if __name__ == '__main__':
    # initiate the board
    board = bl.board.Board()
    # read cells from cells.json
    board.cells_from_json()
    # solve (yet what possible)
    board.find_solution()
    # print the board on console
    board.display()
