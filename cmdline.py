#!/usr/bin/env python
'''
Common command-line option handling.
'''

def parser():
    '''
    Return command line parser with common args defined.  

    Caller should call .parse_args(args) on returned parser object.
    '''
    import argparse
    parser = argparse.ArgumentParser(
        description = 'Sync pages from one wiki to another')
    parser.add_argument('-c', '--config', 
                        help='Set the config file')
    parser.add_argument('-s', '--source',  
                        help='Name of the source wiki')
    parser.add_argument('-d', '--destination', required=True,
                        help='Name of the destination wiki')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force the copy')
    parser.add_argument('pages', nargs='*', 
                        help='Set page(s) to copy, if none then all')
    return parser
