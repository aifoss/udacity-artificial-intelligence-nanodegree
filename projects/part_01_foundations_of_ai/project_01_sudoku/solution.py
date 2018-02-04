
from utils import *


cols_rvrs = cols[::-1]

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# Update the unit list to add the new diagonal units
diag_units = [[rows[i]+cols[i] for i in range(len(rows))],
              [rows[i]+cols_rvrs[i] for i in range(len(rows))]]
unitlist += diag_units

units = dict((box, [unit for unit in unitlist if box in unit]) for box in boxes)
peers = dict((box, set(sum(units[box],[]))-set([box])) for box in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
 
    twin_candidates = [box for box in values.keys() if len(values[box]) == 2]
    
    naked_twins = [[box, peer] for box in twin_candidates for peer in peers[box] \
                   if values[box] == values[peer]]
    
    for naked_twin in naked_twins:
        box1 = naked_twin[0]
        box2 = naked_twin[1]
        twin_val = values[box1]
        common_peers = set(peers[box1]).intersection(set(peers[box2]))
        
        for peer in common_peers:
            for v in twin_val:
                if v in values[peer]:
                    values = assign_value(values, peer, values[peer].replace(v,''))
   
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """

    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    
    for box in solved_boxes:
        digit = values[box]
        
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit, '')
            assign_value(values, peer, values[peer].replace(digit, ''))
    
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    
    stalled = False
    
    while not stalled:
        num_solved_boxes_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        num_solved_boxes_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        stalled = (num_solved_boxes_before == num_solved_boxes_after)
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """

    # First reduce the puzzle
    values = reduce_puzzle(values)
    
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    val_len, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, 
    # and if one returns a value (not False), return that answer!
    for v in values[box]:
        new_values = values.copy()
        new_values[box] = v
        
        solved_values = search(new_values)
        
        if solved_values is not False:
            return solved_values
        
    return False
    

def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    
    values = grid2values(grid)
    values = search(values)
    return values


def values(grid):
    values = {}
    for v, k in zip(grid, boxes):
        values[k] = v
    return values


if __name__ == "__main__":
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '...6..5.....5........2...87..9..1........5.............85.......7..3..5...1.5...9'
    diag_sudoku_grid = '........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2.'
    display(values(diag_sudoku_grid))
    #display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    
    #try:
    #    import PySudoku
    #    PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    #except SystemExit:
    #    pass
    #except:
    #    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
