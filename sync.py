#!/usr/bin/env python
'''
Support for wiki to wiki sync.
'''
import wt

def parse_args(args):
    import argparse
    parser = argparse.ArgumentParser(
        description = 'Sync pages from one wiki to another')
    parser.add_argument('-c', '--config', 
                        help='Set the config file')
    parser.add_argument('-s', '--source',  
                        help='Name of the source wiki')
    parser.add_argument('-d', '--destination', required=True,
                        help='Name of the destination wiki')
    parser.add_argument('--prefix', default="",
                        help='String to prepend to copied wikitext')
    parser.add_argument('--postfix', default="",
                        help='String to append to copied wikitext')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force the copy')
    parser.add_argument('pages', nargs='*', 
                        help='Set page(s) to copy, if none then all')
    return parser.parse_args(args)

def main(args):
    opts = parse_args(args)
    src = wt.Site(opts.source,     opts.config)
    dst = wt.Site(opts.destination, opts.config)

    pages = list(set(opts.pages))
    copied = src.copy(dst, pages=pages, force=opts.force,
                      prefix=opts.prefix, postfix=opts.postfix)
    return copied

if '__main__' == __name__:
    import sys
    copied = main(sys.argv[1:])
    for page in copied:
        print page.title
