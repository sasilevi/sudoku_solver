import math
import copy
import datetime
from logging import Logger


log = Logger(__name__)

colum_value = lambda x: x if x else "__"
cube_size = 0


def create_sudoku():
    return [
        [
            12, None, None, 11, 1, None, None, 7, None, None, 5, 13, None,
            None, 3, 14
        ],
        [
            16, 4, None, 14, None, 11, None, None, None, None, 12, None, 9,
            None, 15, None
        ],
        [
            None, None, 8, 3, None, None, 16, 5, 2, None, None, 9, 13, 4, None,
            None
        ],
        [
            None, 9, 13, 7, None, None, None, 3, 1, None, None, None, 11, 2, 5,
            16
        ],
        [
            3, None, 10, None, None, None, None, 8, 6, None, None, None, None,
            None, None, 9
        ],
        [
            6, 7, None, None, None, 4, 1, 15, 11, None, 13, None, None, None,
            2, None
        ],
        [
            None, None, None, None, None, None, None, None, 5, None, 2, None,
            None, 12, None, None
        ],
        [None, None, 12, 9, 3, 2, 7, None, None, None, 15, 16, 4, 6, None, 5],
        [4, None, 6, 12, 11, 5, None, None, None, 15, 3, 1, 2, 7, None, None],
        [
            None, None, 11, None, None, 15, None, 4, None, None, None, None,
            None, None, None, None
        ],
        [
            None, 3, None, None, None, 13, None, 1, 16, 11, 14, None, None,
            None, 9, 4
        ],
        [
            8, None, None, None, None, None, None, 14, 9, None, None, None,
            None, 5, None, 13
        ],
        [
            7, 12, 3, 10, None, None, None, 2, 15, None, None, None, 5, 16, 14,
            None
        ],
        [
            None, None, 1, 6, 16, None, None, 10, 7, 12, None, None, 15, 13,
            None, None
        ],
        [
            None, 11, None, 16, None, 6, None, None, None, None, 4, None, 10,
            None, 12, 8
        ],
        [
            13, 8, None, None, 15, 3, None, None, 10, None, None, 6, 7, None,
            None, 2
        ],
    ]

def create_sudoku2():
    return [
        [None, None, None, None, 5, None, None, None, 1],
        [4, 5, None, None, None, None, 2, 9, None],
        [None, 6, None, 9, None, 2, 4, None, 7],
        [7, None, None, 6, 4, None, None, None, None],
        [5, 2, None, None, None, None, None, 3, 8],
        [None, None, None, None, 2, 8, None, None, None],
        [8, 4, 6, 3, None, 5, None, 1, None],
        [None, 3, None, None, 8, None, None, 7, None],
        [2, None, None, None, 6, None, None, None, None]
    ]

def print_sudoku(sudoku, message=""):
    print(message)
    rows = len(sudoku)
    for row in sudoku:
        assert rows == len(row)
    log.info(f"sududku is {rows}*{rows}")
    cube_size = int(math.sqrt(rows))
    for ri, row in enumerate(sudoku):
        if ri % cube_size == 0:
            print('|' + '-' * (rows * 4 + cube_size-1), end='|\n')
        for ci, col in enumerate(row):
            if ci == 0:
                print("|", end='')
            if ci != 0 and ci % cube_size == 0:
                print("|", end='')
            print(f"{colum_value(col)}".ljust(4), end='')
        print('|')
    print('|' + '-' * (rows * 4 + cube_size-1), end='|\n'.rjust(2))


def get_cube(sudoku, row, col):
    cube_row = int(int((row / cube_size)) * cube_size)
    cube_col = int(int((col / cube_size)) * cube_size)
    cube = []
    rows = sudoku[cube_row:cube_row + cube_size]
    for r in rows:
        cube.append(r[cube_col:cube_col + cube_size])
    return cube


def validate_row(row):
    v = []
    for x in row:
        if x is not None:
            assert x not in v, f"Value {x} exist multiple times in the row"
            v.append(x)


def validate_col(sudoku, col):
    v = []
    for row in sudoku:
        if row[col] is not None:
            assert row[
                col] not in v, f"Value {row[col]} exist multiple times in col {col}"
            v.append(row[col])


def validate_cube(cube):
    v = []
    for r in cube:
        for x in r:
            if x is not None:
                assert x not in v, f"Value {x} exist multiple times "
                v.append(x)
    # print("OK")


def validate_sudoku(sudoku):
    try:
        for ri, row in enumerate(sudoku):
            validate_row(row)
            for ci, _ in enumerate(row):
                validate_col(sudoku, ci)
                validate_cube(get_cube(sudoku, ri, ci))
    except:
        return False
    return True


def validate_sudoku_change(sudoku, ri, ci):
    try:
        validate_row(sudoku[ri])
        validate_col(sudoku, ci)
        validate_cube(get_cube(sudoku, ri, ci))
    except Exception as e:
        # print(e)
        return False
    return True


def found_solution(sudoku):
    for r in sudoku:
        for c in r:
            if c is None:
                return False
    return True


def solve_sudoku(sudoku):
    # print_sudoku(sudoku)
    solved_sudoku = sudoku
    possibilities = len(sudoku)+1
    for ri, row in enumerate(sudoku):
        for ci, col in enumerate(row):
            if col is None:
                for v in range(1, possibilities):
                    sudoku[ri][ci] = v
                    if not validate_sudoku_change(sudoku, ri, ci):
                        continue
                    solved_sudoku = solve_sudoku(copy.deepcopy(sudoku))
                    if solved_sudoku is None:
                        continue
                    else:
                        return solved_sudoku
                return None

    # print_sudoku(sudoku)
    return solved_sudoku

def get_row_missing_numbers(row):
    result = []
    possibilities = len(row)+1
    for v in range(1, possibilities):
        if v not in row:
            result.append(v) 
    return result

def get_col_missing_numbers(sudoku, ci):
    result = []
    possibilities = len(sudoku)+1
    for v in range(1, possibilities):
        found = False
        for row in sudoku:
            if v == row[ci]:
                found = True
        if not found:
            result.append(v) 
    return result

def get_cube_missing_numbers(sudoku, ri,ci):
    result = []
    possibilities = len(sudoku)+1
    cube = get_cube(sudoku, ri, ci)
    for v in range(1, possibilities):
        found = False
        for r in cube:
            if v in r:
                found = True
                break
        if not found:
            result.append(v)


def optimize_sudoku_rows(sudoku):
    did_optimize = False
    for ri, row in enumerate(sudoku):
        missing_numbers = get_row_missing_numbers(row)
        for n in missing_numbers:
            valid_count = 0
            valid_pos = 0
            for ci, col in enumerate(row):
                if col is None:
                    sudoku[ri][ci] = n
                    if validate_sudoku_change(sudoku,ri,ci):
                        valid_count += 1
                        valid_pos = ci
                    sudoku[ri][ci] = None
                    if valid_count > 1:
                        break
            if valid_count == 1:
                sudoku[ri][valid_pos]=n
                log.info(f"optimize set {n} at row{ri}, col{ci}")
                did_optimize = True
                # print_sudoku(sudoku)
    return did_optimize

def optimize_sudoku_cols(sudoku):
    did_optimize = False
    for ci in range(len(sudoku)):
        missing_numbers = get_col_missing_numbers(sudoku,ci)
        for n in missing_numbers:
            valid_count = 0
            valid_pos_ri = 0
            valid_pos_ci = 0
            for ri, row in enumerate(sudoku):
                if row[ci] is None:
                    sudoku[ri][ci] = n
                    if validate_sudoku_change(sudoku,ri,ci):
                        valid_count += 1
                        valid_pos_ri = ri
                        valid_pos_ci = ci
                    sudoku[ri][ci] = None
                    if valid_count > 1:
                        break
            if valid_count == 1:
                sudoku[valid_pos_ri][valid_pos_ci]=n
                log.info(f"optimize set {n} at row{valid_pos_ri}, col{valid_pos_ci}")
                did_optimize = True
                # print_sudoku(sudoku)
    return did_optimize

def optimize_sudoku(sudoku):
    return optimize_sudoku_rows(sudoku) or optimize_sudoku_cols(sudoku)

def how_much_empty(sudoku):
    count = 0
    for r in sudoku:
        for c in r:
            if c is None:
                count += 1
    return count

def main():
    sudoku = create_sudoku()
    global cube_size 
    cube_size = int(math.sqrt(len(sudoku)))

    print_sudoku(sudoku, "start")
    print(f"empty before optimization:{how_much_empty(sudoku)}")
    while optimize_sudoku(sudoku):
        log.info("Optimization was done")
    print(f"empty After optimization:{how_much_empty(sudoku)}")

    solution = solve_sudoku(sudoku)
    if solution != None:
        print_sudoku(solution, "solution")
    else:
        log.info("Failed to solve!")


if __name__ == "__main__":
    main()
