#!/usr/bin/env python
import wikitools

import os
from ConfigParser import SafeConfigParser, NoSectionError

class Config(object):
    def __init__(self, filename = None, section = None, **kwds):
        if not filename:
            filename = os.path.join(os.path.dirname(__file__),'wt.cfg')

        scp = SafeConfigParser()
        res = scp.read(filename)

        cfg = dict(scp.defaults())
        cfg.update(kwds)

        if section:
            cfg.update(scp.items(section))

        self.__dict__.update(cfg)
        return
    pass

class Site(object):
    def __init__(self, name = None, cfgfile = None):
        '''
        Create a wiki site object with given name as configured in
        config file.  Default cfgfile is wt.cfg in CWD.
        '''
        self.cfg = Config(filename=cfgfile, section=name)
        self.site = wikitools.wiki.Wiki(self.cfg.apiurl)
        self.site.login(self.cfg.username, self.cfg.password)
        return


    def request(self, **params):
        '''
        Make an API request.  Return APIRequest object.
        '''
        write = multipart = False
        if params.has_key('write'):
            write = params.pop('write')
        if params.has_key('multipart'):
            multipart = params.pop('multipart')
        return wikitools.api.APIRequest(self.site, params, write, multipart)

    def query(self, **params):
        '''
        Make a completed query.  Return raw data structure.
        '''
        params.setdefault('action', 'query')
        r = self.request(**params)
        qc = params.get('querycontinue',True)
        return r.query(querycontinue=qc)

    def page(self, name):
        '''
        Return Page object of given name.
        '''
        return wikitools.Page(self.site, title=name)

    def namespaces(self):
        return [(n,p['*']) for n,p in self.site.namespaces.items()]

    def all_pages(self, namespaces = None):
        '''
        Return a list of all page names in all (non-negative) or given
        namespaces.
        '''
        ret = set()
        for nsnum, nsname in self.namespaces():
            if nsnum < 0: 
                continue

            if namespaces and not (nsnum in namespaces or nsname in namespaces):
                continue

            ap = self.query(list='allpages', apnamespace=nsnum)
            for page in ap['query']['allpages']:
                ret.add(page['title'])
        return ret

    def timestamps(self, pages):
        '''
        Return dictionary of page name --> timestamp for given pages.
        '''
        if isinstance(pages,str):
            pages = [pages]

        spages = '|'.join(pages)
        ts = self.query(prop='revisions', rvprop='timestamp', titles=spages)
        ret = {}
        for page in ts['query']['pages'].values():
            if 'missing' in page.keys():
                continue
            tit = page['title']
            ret[tit] = page['revisions'][-1]['timestamp']
        return ret

    def compare(self, other, pages = None):
        '''
        Return a 5-tuple of sets of page names that separates the
        given pages into:

        (only in self, newer in self, same ages, newer in other, only in other)

        Dictionaries map page name to code. 

        If no pages given then all pages from self will be used.
        '''
        if not pages:
            pages = self.all_pages()

        ts1 = self.timestamps(pages)
        ts2 = other.timestamps(pages)

        n1 = set(ts1.keys())
        n2 = set(ts2.keys())
        
        ret = (n1.difference(n2), set(), set(), set(), n2.difference(n1))
        for name in n1.intersection(n2):
            if ts1[name] > ts2[name]:
                ret[1].add(name)
            if ts1[name] == ts2[name]:
                ret[2].add(name)
            if ts1[name] < ts2[name]:
                ret[3].add(name)
            continue
        return ret

    def copy(self, other, pages = None, prefix = "", postfix = "", force=False):
        '''
        Copy the list of pages (or all) from self to other.  

        If either prefix or postfix is given it is prepended or
        appended to the copied page wiki text.

        If force is true, then copy all files regardless of age.

        Return a list of page objects in the other wiki.
        '''
        if not pages:
            pages = self.all_pages()
        if not force:
            comp = self.compare(other, pages)
            pages = list(comp[0]) + list(comp[1])
        ret = []
        for name in pages:
            src = self.page(name)
            dst = other.page(name)
            dst.edit(text=prefix + src.getWikiText() + postfix)
            ret.append(dst)
            continue
        return ret

if '__main__' == __name__:
    import sys
    s = Site(sys.argv[1])
    p = s.page(sys.argv[2])
    print p

    
