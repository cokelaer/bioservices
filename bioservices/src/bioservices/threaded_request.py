import urllib2
import threading


class FetchUrls(threading.Thread):
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
        print 'write done by %s' % self.name
        print 'URL %s fetched by %s' % (self.url, self.name)


urls = [
 "http://rest.kegg.jp/get/path:hsa00010",
  "http://rest.kegg.jp/get/path:hsa00020",
   "http://rest.kegg.jp/get/path:hsa00030",
   "http://rest.kegg.jp/get/path:hsa00040",
   "http://rest.kegg.jp/get/path:hsa00051"
]

def fetchURLs(urls):
    threads = []
    for url in urls:
        t = FetchUrls(url)
        threads.append(t)
    for t in threads:
        t.start()
   
    while sum([t.is_alive() for t in threads]):
        print sum([t.is_alive() for t in threads])

        import time
        time.sleep(1)
    outputs = [t.results for t in threads]

    return outputs



