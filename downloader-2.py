import urllib.request
from lxml import etree
import sqlite3

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


if __name__ == '__main__':

    db = sqlite3.connect("wallpaper.db")

    urls = geturl()

    # update animate alone
    # name =
    # url =
    for name, url in urls.items():
        count = 0
        path = '/Users/GeniusV/Desktop/%s-result.txt' % name
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
                        if (not ifExists(name, link)):
                            file.write(link)
                            file.write('\n')
                            insert(name, link)
                            count = count + 1
                    # store the first link
                    first = p[0].get('data-href')
                    print("%s updates: %d" % name, count)
                else:
                    break
    db.close()

