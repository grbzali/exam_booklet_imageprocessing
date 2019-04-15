import pymysql
import numpy as np
def dbconnect():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='kitapcik')
    return connection

def dbpositions(barcode_id):

    cursor =