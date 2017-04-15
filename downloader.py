# encoding:utf-8

# downloader.py
# version 1.0.0

import urllib.request
from lxml import etree

# This is the script for collecting wall paper download links from wall.alphacoders.com.
# the result will be stored at /Users/GeniusV/Desktop/result.txt
# For default, it will collect from 1st page to 999th page. The number can be changed by changing maxNumber
# This can automatically stop requesting if there is no more pages.


# Attention, this url must contain a 'page=' at the end. When copying the url, DO NOT copy the first page URL.
# Instead, copy the URL of the 2nd page is a better way.
# Finally, remember to delete the last number of the url.

# Gabriel DropOut
# url = 'https://wall.alphacoders.com/by_sub_category.php?id=251328&name=Gabriel+DropOut+Wallpapers&page='

# EroManga-Sensei
url = 'https://wall.alphacoders.com/by_sub_category.php?id=241233&name=EroManga-Sensei+Wallpapers&page='

maxNumber = 999
first = None
count = 0

# open the file to store the result
with open('/Users/GeniusV/Desktop/result.txt', 'w') as file:
    # loop for the real urls containing the links
    for currentNumber in range(1, maxNumber):
        realUrl = url + str(currentNumber)
        data = urllib.request.urlopen(realUrl)
        html = data.read()
        page = etree.HTML(html)

        # get all nodes contains the link
        p = page.xpath(u"//span[@title='Download Wallpaper!']")

        # check if the link has been collected. If false, loop will break, if
        # true , store the links.
        if first != p[0].get('data-href'):
            # get node contain the link
            for arg in p:
                # output
                file.write(arg.get('data-href'))
                file.write('\n')
                count = count + 1
            # store the first link
            first = p[0].get('data-href')
            print(realUrl)
        else:
            break

print("total: " + str(count))
