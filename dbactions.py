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
    positions = cursor.fetchall()

    if positions == 0:
        print("Barcode id'e ait bilgi bulunmuyor...")
        return 0

    else:

        positions = positions[0][0][1:len(positions[0][0]) - 1]

        sql = "SELECT aday_id FROM barcode WHERE barcode_id = %s"
        cursor.execute(sql, barcode_id)
        aday_id = cursor.fetchall()
        aday_id = aday_id[0][0]
        cursor.close()

    return positions, aday_id

def dbinsert (connection, aday_id, kitapcik_id, cevaplar):

    result = 0
    cursor = connection.cursor()
    sql = "SELECT * FROM test_cevaplar where aday_id = %s and kitapcik_id = %s"
    cursor.execute(sql, (aday_id, kitapcik_id))
    result = cursor.fetchall()

    if not result:
        print(result)
        sql = "INSERT INTO test_cevaplar (id, aday_id, kitapcik_id, cevaplar) VALUES (NULL, %s, %s, %s)"
        cursor.execute(sql, (aday_id, kitapcik_id, cevaplar))
        connection.commit()
        print("Kayıt Eklendi...")

    else:

        print("Aynı aday ve kitapçığa ait cevap kaydı bulunuyor...!")



