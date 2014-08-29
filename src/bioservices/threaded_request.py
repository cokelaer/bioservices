import urllib2
import threading



class RequestURL(threading.Thread):
    """
    Thread checking URLs.
    No need for communication
    """

    def __init__(self, url):
        """
        Constructor.

        @param urls list of urls to check
        @param output file to write urls output
        """
        threading.Thread.__init__(self)
        self.url = url
        self.results = None

    def run(self):
        """
        Thread run method. Check URLs one by one.
        """
        req = urllib2.Request(self.url)
        try:
            d = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print 'URL %s failed: %s' % (url, e.reason)
        self.results = d.read()
        #print 'write done by %s' % self.name
        #print 'URL %s fetched by %s' % (self.url, self.name)


_urls = [
   "http://rest.kegg.jp/get/path:hsa00010",
   "http://rest.kegg.jp/get/path:hsa00020",
   "http://rest.kegg.jp/get/path:hsa00030",
   "http://rest.kegg.jp/get/path:hsa00040",
   "http://rest.kegg.jp/get/path:hsa00051"
]

class RequestMultiURL(object):
    def __init__(self):
        self.threads = []
    def reset(self):
        self.threads = []
    def add_url(self, url):
        t = RequestURL(url)
        self.threads.append(t)
    def start(self):
        for t in self.threads:
            t.start()
    def is_alive(self):
        s = sum([t.is_alive() for t in self.threads])
        if s > 0:
            return True
        else:
            return False

    def wait(self):
        import time
        while self.is_alive():
            time.sleep(1)
    def get_results(self):
        return [t.results for t in self.threads]


#s = RequestMultiURL()
#for u in _urls:
#    s.add_url(u)
#s.start()
#s.wait()
#s.get_results()
