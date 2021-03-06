import os
import re
import sqlite3
import urllib.request

import shutil
from lxml import etree
from tqdm import tqdm

maxNumber = 999
first = None
count = 0


# open the file to store the result
# the result will be stored at /Users/GeniusV/Desktop/result.txt

def insert(tablename, address):
    try:
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
    create_table = '''create table %s
        (address text UNIQUE )
        ''' % (tablename)
    print("Creating table %s..." % tablename)
    db.execute(create_table)
    db.commit()


def geturl():
    sql = '''select * from animate'''
    result = db.execute(sql)
    dict = {}
    for row in result:
        dict[row[0]] = row[1]
    return dict


def ifExists(tablename, address):
    try:
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


if __name__ == '__main__':

    try:
        big_bar = tqdm(total = 1000)
        print("Script is running...")
        print("Connecting database...")
        db = sqlite3.connect("wallpaper.db")
        print("Getting animate links...")
        urls = geturl()

        # update animate alone
        # name =
        # url =
        for name, url in urls.items():
            count = 0
            os.makedirs('/Users/GeniusV/Desktop/%s/' % name)
            path = '/Users/GeniusV/Desktop/%s/%s-result.txt' % (name, name)
            print("Creating file %s..." % path)

            with open(path, 'w') as file:
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
                        print("Working on " + realUrl)
                        for arg in p:
                            # output
                            link = arg.get('data-href')
                            num = get_img_id(link)
                            if not ifExists(name, num):
                                file.write(link)
                                file.write('\n')
                                insert(name, num)
                                count += 1
                        # store the first link
                        first = p[0].get('data-href')
                        print("%s updates: %d" % (name, count))
                    else:
                        break

            if count == 0:
                shutil.rmtree('/Users/GeniusV/Desktop/%s' % name)

    except Exception as e:
        raise e
    finally:
        db.close()


