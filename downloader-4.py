import os
import re
import shutil
import sqlite3
import threading
import urllib.request
from urllib import request

from lxml import etree

first = None
count = 0


class Count:
    i = 0


# open the file to store the result
# the result will be stored at /Users/GeniusV/Desktop/result.txt

def insert(tablename, address):
    try:
        db = sqlite3.connect(db_address)
        sql = '''insert into %s VALUES ('%s')
''' % (tablename, address)
        # print("Inserting  %s..."% tablename)
        db.execute(sql)
        db.commit()
    except sqlite3.OperationalError as e:
        if str("no such table: " + tablename) == str(e):
            createTable(tablename)
            insert(tablename, address)
        else:
            raise e


def createTable(tablename):
    db = sqlite3.connect(db_address)
    create_table = '''create table %s
        (address text UNIQUE )
        ''' % (tablename)
    print("Creating table %s..." % tablename)
    db.execute(create_table)
    db.commit()


def geturl():
    db = sqlite3.connect(db_address)
    sql = '''select * from animate'''
    result = db.execute(sql)
    dict = {}
    for row in result:
        dict[row[0]] = row[1]
    return dict


def ifExists(tablename, address):
    try:
        db = sqlite3.connect(db_address)
        sql = '''select * from %s where address='%s'
        ''' % (tablename, address)
        result = db.execute(sql).fetchall()
        if (len(result)) == 0:
            return False
        else:
            return True
    except sqlite3.OperationalError as e:
        if str("no such table: " + tablename) == str(e):
            createTable(tablename)
            ifExists(tablename, address)


def getCount(table_name):
    try:
        db = sqlite3.connect(db_address)
        sql = '''select count(*) as count from %s''' % (table_name)
        result = db.execute(sql)
        ans = result.fetchone()[0]
        return ans
    except sqlite3.OperationalError as e:
        raise e


def get_img_id(address):
    m = re.match("https://initiate.alphacoders.com/download/wallpaper/(\d+)/", address)
    return m.group(1)


def get_img_count(page):
    result = page.xpath(u'/html/body/h1/i')
    print(result[0].text)


def download(url, output):
    file_name = url.split('/')[-4]
    suffix = url.split('/')[-2]
    file_path = output + str(file_name + '.' + suffix)
    with request.urlopen(url) as web:
        with open(file_path, 'wb') as outfile:
            outfile.write(web.read())
            print("download finish: " + str(url))


def do_page(realUrl, name, lock, count):
    data = urllib.request.urlopen(realUrl)
    html = data.read()
    page = etree.HTML(html)

    # get all nodes contains the link
    p = page.xpath(u"//span[@title='Download Wallpaper!']")

    # check if the link has been collected. If false, loop will break, if
    # true , store the links.

    # get node contain the link
    print("Working on " + realUrl)
    for arg in p:
        # output
        link = arg.get('data-href')
        num = get_img_id(link)
        if not ifExists(name, num):
            thread = threading.Thread(target = download, args = (link, "/Users/GeniusV/Desktop/" + name + "/"))
            thread.start()
            insert(name, num)
            if lock.acquire():
                count.i += 1
                lock.release()

    print("%s updates: %d" % (name, count.i))


def do_animate(name, url):
    count = Count()
    os.makedirs('/Users/GeniusV/Desktop/%s/' % name)
    maxNumber = get_total_page(url) + 1
    lock = threading.Lock()
    thread_list = []
    for currentNumber in range(1, maxNumber):
        realUrl = url + str(currentNumber)
        thread = threading.Thread(target = do_page, args = (realUrl, name, lock, count))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    if count.i == 0:
        shutil.rmtree('/Users/GeniusV/Desktop/%s' % name)


def get_total_page(url):
    real_url = url + str(1)
    data = urllib.request.urlopen(real_url)
    html = data.read()
    page = etree.HTML(html)
    p = page.xpath(u"//a[@id='next_page']/../../li[last()-1]/a")
    return int(p[0].text)


if __name__ == '__main__':

    try:
        print("Script is running...")
        print("Connecting database...")
        db_address = "wallpaper.db"

        print("Getting animate links...")
        urls = geturl()
        # update animate alone
        # name =
        # url =
        for name, url in urls.items():
            thread = threading.Thread(target = do_animate, args = (name, url))
            thread.start()

    except Exception as e:
        raise e
        for name, url in urls.items():
            thread = threading.Thread(target = do_animate, args = (name, url))
            thread.start()
