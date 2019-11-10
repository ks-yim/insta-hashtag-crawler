from gevent import monkey; monkey.patch_all()

import gevent.pool
import gevent.queue
import os.path
import json
import requests
import csv
import enum
from collections import namedtuple
from datetime import datetime

Endpoint = namedtuple('Endpoint', 'url type tagname')
EndpointType = enum.IntEnum('EndpointType', 'POST TAG')

class Crawler(object):
    """A very simple queued gevent web crawler"""
    ENDPOINT_ROOT = 'https://www.instagram.com/explore/%s/%s/?__a=1'
    def __init__(self, *tagnames):
        self._running = True
        self._pool = gevent.pool.Pool(30)
        self._queue = gevent.queue.PriorityQueue()
        self._tagnames = tagnames
        self._crawled = 0
        self._TAG_ENDPOINT = self.ENDPOINT_ROOT % ('tags', '%s')
        self._POST_ENDPOINT = self.ENDPOINT_ROOT % ('p', '%s')
        self._end_cursor = gevent.queue.Queue()
        self._f = open(
            self._get_csv_path(),
            'a+',
            encoding='utf8'
        )
        self._set_csv_writer()


    def _set_csv_writer(self):
        self._csv_writer = csv.DictWriter(
            self._f,
            fieldnames=['id', 'tag', 'shortcode', 'username', 'text', 'taken_at']
        )
        self._csv_writer.writeheader()

    def _get_csv_path(self, nth=None):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            self._tagnames[0] + '_' + datetime.now().strftime('%Y%m%d')
        )
        nth = nth if nth is not None else 0
        path_ = path + '(%d)' % nth + '.csv'
        while os.path.exists(path_):
            path_ = path + '(%d)' % nth + '.csv'
            nth += 1

        print(path_)
        return path_

    def _get_post_endpoint(self, tagname, shortcode):
        return (10, Endpoint(
            self._POST_ENDPOINT % shortcode,
            EndpointType.POST,
            tagname,
        ))
    
    def _get_tag_endpoint(self, tagname, end_cursor=None):
        base = self._TAG_ENDPOINT % tagname
        url = base if end_cursor is None else base + '&max_id=%s' % end_cursor
        return (0, Endpoint(
            url,
            EndpointType.TAG,
            tagname,
        ))

    def _q_put(self, endpoint):
        if self._running:
            self._queue.put(endpoint)

    def crawl(self):
        for tagname in self._tagnames:
            self._q_put(
                self._get_tag_endpoint(tagname)
            )
        self._pool.spawn(self._crawl)

        while not (self._queue.empty() and self._pool.free_count() == 30):
            gevent.sleep(0.1)
            for i in range(0, min(self._queue.qsize(), self._pool.free_count())):
                self._pool.spawn(self._crawl)

        print('called join')
        self._pool.join()

    def _crawl(self):
        while True:
            if self._queue.qsize() < 100:
                try:
                    end_cursor = self._end_cursor.get(timeout=0)
                except gevent.queue.Empty:
                    pass
                else:
                    self._q_put(
                        self._get_tag_endpoint(self._tagnames[0], end_cursor=end_cursor)
                    )
            try:
                endpoint = self._queue.get(timeout=0)[1]
            except gevent.queue.Empty:
                break
            
            if endpoint.type == EndpointType.POST:
                self.crawl_post(endpoint)
            elif endpoint.type == EndpointType.TAG:
                self.crawl_tag(endpoint)

    def crawl_tag(self, endpoint):
        def fetch():
            res = requests.get(endpoint.url)
            if res.status_code == 429:
                print('[status_code: %d] %s' %(res.status_code, endpoint.url))
                print('sleep for the rate limit...')
                gevent.sleep(10)
            elif res.status_code == 200:
                print('[status_code: %d] %s' %(res.status_code, endpoint.url))
                return json.loads(res.text)
            else:
                raise requests.exceptions.RequestException()
        
        data = None
        while data is None:
            data = fetch()

        has_next = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        edges    = data['graphql']['hashtag']['edge_hashtag_to_media']['edges']

        if has_next:
            end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            ## hash_tag = data['graphql']['hashtag']['name']
            self._end_cursor.put(end_cursor)

        for edge in edges:
            shortcode = edge['node']['shortcode']
            self._q_put(
                self._get_post_endpoint(endpoint.tagname, shortcode)
            )

    def crawl_post(self, endpoint):
        def fetch():
            res = requests.get(endpoint.url)
            if res.status_code == 429:
                print('[status_code: %d] %s' %(res.status_code, endpoint.url))
                print('sleep for the rate limit...')
                gevent.sleep(10)
            elif res.status_code == 200:
                self._crawled += 1
                print('[status_code: %d, total_fetched: %d] %s' %(res.status_code, self._crawled, endpoint.url))
                return json.loads(res.text)
            else:
                raise requests.exceptions.RequestException()
        
        data = None
        while data is None:
            data = fetch()

        username = data['graphql']['shortcode_media']['owner']['username']
        try:
            text = data['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            text = None
        taken_at_ts = data['graphql']['shortcode_media']['taken_at_timestamp']
        shortcode = data['graphql']['shortcode_media']['shortcode']

        if self._crawled % 500 == 0:
            self._f.close()
            self._f = open(self._get_csv_path(nth=self._crawled // 500), 'a+', encoding='utf8')
            self._set_csv_writer()

        self._csv_writer.writerow({
            'id': self._crawled,
            'tag': endpoint.tagname,
            'shortcode': shortcode,
            'username': username,
            'text': text,
            'taken_at': str(datetime.fromtimestamp(taken_at_ts))
        })

    def stop(self):
        self._running = False
        self._pool.join()

    def __del__(self):
        self._f.close()

if __name__ == '__main__':
    c = Crawler('연착')
    try:
        c.crawl()
    except KeyboardInterrupt:
        c.stop()
        print('closing crawler...')
        print('total fetched posts: %d' % c._crawled)