import sys
import os.path
import argparse
from .crawler import Crawler

parser = argparse.ArgumentParser()
parser.add_argument('hashtag', help='')
parser.add_argument('-q', '--quiet', help='', action='store_true')
parser.add_argument('-d', '--dir', help='', type=str)
args = parser.parse_args()

def crawl():
    c = Crawler(args.hashtag)
    #: Handle optional arguments
    if args.quiet is True:
        f = open(os.devnull, 'w')
        sys.stdout = f

    if args.dir is not None:
        if not os.path.isdir(args.dir):
            raise ValueError('argument for [-d][--dir] served is must be an existing directory')
        c.set_csv_path(os.path.abspath(args.dir))
    try:
        c.crawl()
    except KeyboardInterrupt:
        c.stop()
        print('closing crawler...')
        print('total fetched posts: %d' % c._crawled)