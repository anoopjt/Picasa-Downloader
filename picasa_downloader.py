#Author: Anoop Jacob Thomas<anoopjt@gmail.com>
#Email: anoopjt@gmail.com
#Web: http://anoop.caremedia.org
#License: GPLv3 or later

from urllib2 import urlopen
from os.path import basename, join
from os import mkdir
from urlparse import urlsplit
from BeautifulSoup import BeautifulStoneSoup
import sys
import time

# Based on http://stackoverflow.com/a/3160819
class ProgressBar(object):
    def __init__(self, items):
        self.display_width = 40
        self.items = items

    def update(self, n):
        complete_frac = (float(n+1)/self.items)
        complete = int(complete_frac * self.display_width)
        remaining = self.display_width-complete
        info = '%4.0f%% Done' %(complete_frac * 100,)
        sys.stdout.write('[%s%s]%s' %('-' * complete, ' ' * remaining, info))
        sys.stdout.flush()
        if complete < self.display_width:
            # add 2 to account for brackets [ ]
            sys.stdout.write('\b' * (self.display_width+len(info)+2))
        else:
            sys.stdout.write('\n')

feedurl = False
url = raw_input('Enter the Picasa web album/feed url : ')
# Code for getting address of picasa web
if urlsplit(url).path.startswith('/data/feed/'): #if the link given is a feed - picasaweb
    feedurl = True
    #print "Path is a feed path"
elif urlsplit(url).netloc == "picasaweb.google.com":
    y = urlopen(url).read()
    soup = BeautifulStoneSoup(y,selfClosingTags=['meta','link','base'])
    for link in soup.findAll('link'):
        if link.has_key('rel'):
            if link['rel']=="alternate":
                url = link['href']
                feedurl = True
                #print "Feed path found", url
                break
name_album = raw_input('Enter name of Album : ')
mkdir(name_album)
x = urlopen(url)
y = x.read()
tags = BeautifulStoneSoup(y).findAll('media:content')
print len(tags), "pictures found!"
progress_bar = ProgressBar(len(tags))
for i, each in enumerate(tags):
    if each.has_key('url'):
        img = urlopen(each['url']).read()
        fname = join(name_album,basename(urlsplit(each['url'])[2]))
        output = open(fname,'wb')
        output.write(img)
        output.close()
        progress_bar.update(i)

