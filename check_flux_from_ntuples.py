#!/bin/env python

import argparse

def makeParser():
    parser = argparse.ArgumentParser(
        prog='check_flux_from_ntuples.py',
        description="""script to check the g4numi flux entries.""",
        epilog="Any questions or comments to laliaga@fnal.gov")
    
    parser.add_argument('-l', '--list-file', help="input list file of G4NuMI files (dk2nu format)")
    parser.add_argument('-o', '--output-file', help="output root file")

    return vars(parser.parse_args())


if __name__ == "__main__":
    opts = makeParser()
    from ana import process_list
    if opts['list_file'] is None:
        raise ValueError("You must provide a file with a list of input files!")
    elif opts['output_file'] is None:
        raise ValueError("You must provide an output file!")
    else:
        process_list(opts['list_file'], opts['output_file'])
        
