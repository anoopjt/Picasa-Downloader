#Author: Anoop Jacob Thomas<anoopjt@gmail.com>
#Email: anoopjt@gmail.com
#Web: http://anoop.caremedia.org
#License: GPLv3 or later

from urllib2 import urlopen
from os.path import basename, join
from os import mkdir
from urlparse import urlsplit
from BeautifulSoup import BeautifulStoneSoup

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
for each in tags:
    if each.has_key('url'):
        img = urlopen(each['url']).read()
        fname = join(name_album,basename(urlsplit(each['url'])[2]))
        output = open(fname,'wb')
        output.write(img)
        output.close()

# Obsolete code
#pics = []
#for l in y.split():
#    if l.startswith('url='):
#        pics.append(l.split("'")[1])
# pics_set = set(pics)
# for each in pics_set:
#     img = urlopen(each).read()
#     fname = basename(urlsplit(each)[2])
#     output = open(fname,'wb')
#     output.write(img)
#     output.close()
#     raw_input('Press enter to continue')
