import pymysql
import numpy as np

def dbconnect():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='belgelendirme')
    return connection

def dbgetbarcode(connection, barcode_id):
    result = []

    cursor = connection.cursor()
    sql = "SELECT positions FROM barcode WHERE barcode_id = %s"
    cursor.execute(sql, barcode_id)
    result = cursor.fetchall()
    cursor.close()
    result = result[0][0][1:len(result[0][0]) - 1]


    return result

def dbinsert (connection, aday_id, kitapcik_id, cevaplar):

    result = 0
    cursor = connection.cursor()
    sql = "SELECT * FROM test_cevaplar where aday_id = %s and kitapcik_id = %s"
    cursor.execute(sql, (aday_id, kitapcik_id))
    result = cursor.fetchall()

    if not result:

        sql = "INSERT INTO test_cevaplar (id, aday_id, kitapcik_id, cevaplar) VALUES (NULL, %s, %s, %s)"
        cursor.execute(sql, (aday_id, kitapcik_id, cevaplar))
        connection.commit()
        print("Kayıt Eklendi...")
    else:

        print("Aynı aday ve kitapçığa ait cevap kaydı bulunuyor...!")


barcode = 6070014
connection = dbconnect()
pos = dbgetbarcode(connection, barcode)
print(pos)

dbinsert(connection, 4, 1, "aaaocobxaabxob")

