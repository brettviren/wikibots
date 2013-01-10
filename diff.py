#!/usr/bin/env python
'''
Display the difference between wikis
'''
import os
import sys
import wt
import cmdline
import difflib

def main(args):
    parser = cmdline.parser()
    parser.add_argument('-o','--output',help='Set output file pattern.')

    opts = parser.parse_args(args)
    src = wt.Site(opts.source,     opts.config)
    dst = wt.Site(opts.destination, opts.config)

    pages = list(set(opts.pages))

    for count, section in enumerate(src.diff(dst,pages)):
        count += 1
        if opts.output:
            fname = opts.output
            if '%' in fname:
                fname %= count
            else:
                fname = str(count).join(os.path.splitext(fname))
            fp = open(fname,'w')
        else:
            fp = sys.stdout
         
        for ud in section.values():
            fp.write('\n'.join([line for line in ud]))
            fp.write('\n')
            continue
        continue
    return

if '__main__' == __name__:
    import sys
    main(sys.argv[1:])
