#!/usr/bin/env python
'''
Support for wiki to wiki sync.
'''
import wt
import cmdline

def parse_args(args):
    parser = cmdline.parser()
    parser.add_argument('--prefix', default="",
                        help='String to prepend to copied wikitext')
    parser.add_argument('--postfix', default="",
                        help='String to append to copied wikitext')
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
