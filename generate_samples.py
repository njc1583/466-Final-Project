#!/bin/python

"""
USAGE
$ python3 generate_samples.py --filename=INPUT_MATRIX_FILENAME
                            --outfile=SOLUTIONS_OUTFILE
                            --timeout=TIMEOUT
                            --num_samples=NUMBER_OF_SAMPLES
                            --sampler=SAMPLER_TYPE
                            --s=NUM_CELL_CLUSTERS
                            --t=NUM_MUTATION_CLUSTERS
                            --allowed_losses=LOSSES_FILENAME
                            --debug

Generates samples for matrix in INPUT_MATRIX_FILENAME and saves reconstructed k-Dollo matrices to
SOLUTIONS_OUTFILE.
"""

from generate_formula import read_matrix, get_cnf
from get_vars import write_vars
from reconstruct_solutions import reconstruct_solutions

import sys
import time
import os 
import argparse
import platform

def unigensampler_generator(infile, outfile, num_samples, timeout):
    unigen_cmd = f'./samplers/unigen --samples={num_samples} --maxTotalTime={timeout} {infile} {outfile}'

    os.system(unigen_cmd)

def quicksampler_generator(cnf_file, num_samples, timeout, osname):
    q_cmd = f'./samplers/quicksampler -n {num_samples} -t {timeout} {cnf_file}'
    z3_cmd = f'./samplers/z3 sat.quicksampler_check=true {cnf_file}'

    if osname == 'macOS':
        q_cmd = f'./samplers/macOS/quicksampler -n {num_samples} -t {timeout} {cnf_file}'
        z3_cmd = f'./samplers/macOS/z3 sat.quicksampler_check=true {cnf_file}'

    os.system(q_cmd)
    os.system(z3_cmd)

def convert_unigen_to_quicksample(unigen_outfile, samples_outfile):
    unigen_file = open(unigen_outfile, 'r')
    samples_file = open(samples_outfile, 'w')

    unigen_lines = unigen_file.readlines()

    for unigen_sample in unigen_lines:
        samples_file.write(f'{unigen_sample.strip()[1:]}\n')

    unigen_file.close()
    samples_file.close()

def clean_up(shortened_filename, unigen):
    remove_formula = f'rm {shortened_filename}.tmp.formula.cnf'
    remove_samples = f'rm {shortened_filename}.tmp.formula.cnf.samples'
    remove_valid = f'rm {shortened_filename}.tmp.formula.cnf.samples.valid'
    remove_vars = f'rm {shortened_filename}.variables'

    os.system(remove_formula)
    os.system(remove_valid)
    os.system(remove_vars)

    if unigen:
        remove_unigen_file = f'rm {shortened_filename}.tmp.formula.cnf.unigen'
        os.system(remove_unigen_file)
    else:
        os.system(remove_samples)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate samples for given directories')

    parser.add_argument(
        '--filename',
        type=str,
        default='data/example.txt',
        help='The input file containing the matrix to generate samples for'
    )
    parser.add_argument(
        '--outfile',
        type=str,
        default='solutions.txt',
        help='Outfile to write solutions to'
    )
    parser.add_argument(
        '--timeout',
        type=float,
        default=7200.0,
        help='Timeout for samplers (seconds), default is 7200'
    )
    parser.add_argument(
        '--num_samples',
        type=int,
        default=10000,
        help='number of samples to generate'
    )
    parser.add_argument(
        '--sampler',
        type=int,
        default=1,
        help='1 to use Quicksampler, 2 to use Unigen.'
    )
    parser.add_argument(
        '--s',
        type=int,
        default=1,
        help='Number of cell clusters to use.'
    )
    parser.add_argument(
        '--t',
        type=int,
        default=1,
        help='Number of mutation clusters to use.'
    )
    parser.add_argument(
        '--allowed_losses',
        type=str,
        default=None,
        help='Filename containing allowed mutation losses, listed on one line, separated by commas.'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug mode'
    )

    parser.set_defaults(debug=False)

    os_name = ''

    if platform.system() == "linux" or platform.system() == "linux2":
        os_name = 'linux'
    elif platform.system() == "Darwin":
        os_name = 'macOS'
    elif platform.system() == "win32":
        os_name = 'win'

    args = parser.parse_args()

    shortened_filename = args.filename.split('.')[0]
    cnf_filename = f'{shortened_filename}.tmp.formula.cnf'
    variables_filename = f'{shortened_filename}.variables'

    variables = get_cnf(args.filename, cnf_filename, args.s, args.t, args.sampler == 2, args.allowed_losses)
    write_vars(variables_filename, variables)

    if args.sampler == 1:
        quicksampler_generator(cnf_filename, args.num_samples, args.timeout, os_name)
        valid_solutions = f'{shortened_filename}.tmp.formula.cnf.samples.valid'
        reconstruct_solutions(args.filename, valid_solutions, args.outfile, variables, args.debug)
        if not args.debug:
            clean_up(shortened_filename, False)
    else:
        if os_name == 'macOS':
            print('Unigen not compatible with OS X')
        else:
            unigen_outfile = cnf_filename + '.unigen'
            samples_outfile = cnf_filename + '.samples.valid'

            unigensampler_generator(cnf_filename, unigen_outfile, args.num_samples, args.timeout)
            convert_unigen_to_quicksample(unigen_outfile, samples_outfile)

            valid_solutions = f'{shortened_filename}.tmp.formula.cnf.samples.valid'
            reconstruct_solutions(args.filename, valid_solutions, args.outfile, variables, args.debug)
            if not args.debug:
                clean_up(shortened_filename, True)