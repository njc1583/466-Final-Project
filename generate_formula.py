from get_clauses import *
from get_vars import create_variable_matrices, write_vars

import sys
import os
import time
import argparse

"""
USAGE
$ python3 generate_formula.py --filename=INPUT_MATRIX_FILENAME
                            --outfile=FORMULA_FILENAME
                            --s=NUM_CELL_CLUSTERS
                            --t=NUM_MUTATION_CLUSTERS
                            --allowed_losses=LOSSES_FILENAME
                            --sampler=SAMPLER_TYPE

Generates a boolean formula in CNF format that maps the matrix in INPUT_MATRIX_FILENAME
to a smaller 1 dollo matrix with NUM_CELL_CLUSTERS rows and NUM_MUTATION_CLUSTERS where only losses
specified in LOSSES_FILENAME are allowed. The formula is in the format required by SAMPLER_TYPE and is
written to FORMULA_FILENAME.
"""

def get_cnf(read_filename, write_filename, s=5, t=5, unigen=True, losses_filename=None):
    """
    Writes a cnf formula for matrix specified in read_filename to write_filename using s
    rows and t columns for clustered matrix.

    read_filename - file containing input matrix
    write_filename - file to write formula to
    s - number of rows in clustered matrix/cell clusters
    t - number of columns in clustered matrix/mutation clusters
    """
    matrix = read_matrix(read_filename)

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    variables = create_variable_matrices(matrix, s, t)
    allowed_losses = parse_allowed_losses(losses_filename, len(matrix[0]))

    false_positives = variables['false_positives']
    false_negatives = variables['false_negatives']

    pair_in_col_equal = variables['pair_in_col_equal']
    pair_in_row_equal = variables['pair_in_row_equal']

    col_is_duplicate = variables['col_is_duplicate']
    row_is_duplicate = variables['row_is_duplicate']

    is_two = variables['is_two']
    is_one = generate_is_one(matrix, false_positives, false_negatives, is_two)
    
    # get clauses
    forbidden_clauses  = get_clauses_no_forbidden(is_one, is_two, row_is_duplicate, col_is_duplicate)
    not_one_and_two_clauses = get_clauses_not_one_and_two(is_one, is_two)

    # one_fp = constrain_fp(false_positives)
    # one_fn = constrain_fp(false_negatives)

    row_duplicate_clauses = get_row_duplicate_clauses(pair_in_col_equal, row_is_duplicate)
    col_duplicate_clauses = get_col_duplicate_clauses(pair_in_row_equal, col_is_duplicate)

    col_pairs_equal_clauses = get_col_pairs_equal_clauses(is_one, is_two, pair_in_col_equal)
    row_pairs_equal_clauses = get_row_pairs_equal_clauses(is_one, is_two, pair_in_row_equal)

    one_row_duplicate = constrain_fp(row_is_duplicate, False)
    one_col_duplicate = constrain_fp(col_is_duplicate, False)

    at_least_one_row_dup = at_least_one(row_is_duplicate)
    at_least_one_col_dup = at_least_one(col_is_duplicate)

    first_line = ''
    if unigen:
        num_clauses = len(forbidden_clauses) + len(not_one_and_two_clauses)
        # num_clauses += len(one_fp) + len(one_fn)
        num_clauses += len(row_duplicate_clauses) + len(col_duplicate_clauses)
        num_clauses += len(col_pairs_equal_clauses) + len(row_pairs_equal_clauses)
        num_clauses += len(one_row_duplicate) + len(one_col_duplicate)
        num_clauses += len(at_least_one_row_dup) + len(at_least_one_col_dup)
        
        num_vars = col_is_duplicate[num_cols-1]

        first_line = f'p cnf {num_vars} {num_clauses}\n'

    with open(write_filename, 'w') as f:
        if unigen:
            f.write(first_line)
        f.writelines(forbidden_clauses)
        f.writelines(not_one_and_two_clauses)

        # f.writelines(one_fp)
        # f.writelines(one_fn)

        f.writelines(row_duplicate_clauses)
        f.writelines(col_duplicate_clauses)

        f.writelines(col_pairs_equal_clauses)
        f.writelines(row_pairs_equal_clauses)

        f.writelines(one_row_duplicate)
        f.writelines(one_col_duplicate)

        f.writelines(at_least_one_row_dup)
        f.writelines(at_least_one_col_dup)

    return variables

def parse_allowed_losses(filename, num_mutations):
    if not filename:
        return set([i for i in range(num_mutations)])
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            allowed = lines[0].split(',')
            return set([int(i) for i in allowed])
        else:
            return set()

def read_matrix(filename):
    """
    Returns matrix parsed from given file.
    First two lines of matrix file must specify number of cells and mutations of input.

    For example:
    5 # cells
    5 # mutations
    0 1 0 0 0
    0 0 1 0 1
    0 0 0 0 0
    0 0 0 0 0
    1 0 0 1 0

    filename - file that contains input matrix
    """
    matrix_file = open(filename, 'r')
    lines = matrix_file.readlines()[2:]
    
    return [[int(x) for x in line.split()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate samples for given directories')

    parser.add_argument(
        '--filename',
        type=str,
        default='data/example.txt',
        help='the input file containing the matrix to generate samples for'
    )
    parser.add_argument(
        '--outfile',
        type=str,
        default='formula.cnf',
        help='outfile to write formula to'
    )
    parser.add_argument(
        '--s',
        type=int,
        default=5,
        help='number of rows in clustered matrix'
    )
    parser.add_argument(
        '--t',
        type=int,
        default=5,
        help='number of columns in clustered matrix'
    )
    parser.add_argument(
        '--sampler',
        type=int,
        default=1,
        help='1 to use Quicksampler, 2 to use Unigen.'
    )
    parser.add_argument(
        '--allowed_losses',
        type=str,
        default=None,
        help='Filename containing allowed mutation losses, listed on one line, separated by commas.'
    )

    args = parser.parse_args()

    filename = args.filename
    outfile = args.outfile
    s = args.s
    t = args.t

    start = time.time()
    variables = get_cnf(filename, outfile, s, t, args.sampler == 2, args.allowed_losses)
    end = time.time()

    write_vars("formula.vars", variables)

    print(f'Generated cnf formula in {end - start} seconds')