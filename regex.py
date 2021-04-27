import re
from time import process_time
import mysql.connector
from datetime import datetime

mysqldb = mysql.connector.connect(host='localhost', user='root',passwd='', database='reminder')
curs = mysqldb.cursor()
#text = "Halo tolong dicatat ya matkul IF2230 ada tucil materi string matching 05 april 2021"

def addTask(tes):
    text = tes.lower()
    arr = []
    month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    re_matkul = '([a-zA-Z]{2}[0-9]{4})'
    re_jenis = 'kuis|tucil|tubes|ujian|praktikum|rangkuman'
    re_tgl = '[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}'
    re_materi = '(materi |tentang |mengenai )+(.*)'
    x1 = re.findall(re_tgl,text)
    if(x1):
        #arr.append(x1[0])
        patt = '[0-9]{2}[/][0-9]{2}[/][0-9]{4}'
        patt2 = '[0-9]{2}[-][0-9]{2}[-][0-9]{4}'
        if(re.search(patt,text)):
            tanggal = str(x1[0]).split('/')
            arr.append(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
            text=text.replace(x1[0],"")
        elif(re.search(patt2,text)):
            tanggal = str(x1[0]).split('-')
            arr.append(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
            text=text.replace(x1[0],"")
        else:
            tanggal = str(x1[0]).split()
            bulan = 0
            for i in range(12):
                if(tanggal[1]==month[i]):
                    bulan=i+1
                    if(bulan<10):
                        bulan = '0'+str(bulan)
                    else:
                        bulan = str(bulan)
            arr.append(tanggal[2]+'/'+bulan+'/'+tanggal[0])
            text=text.replace(x1[0],"")

    x2 = re.findall(re_matkul,text)
    if(x2):
        arr.append(x2[0])
        text=text.replace(x2[0],"")

    x3 = re.findall(re_jenis,text)
    if(x3):
        arr.append(x3[0])
        text=text.replace(x3[0],"")

    x4 = re.findall(re_materi,text)
    if(x4):
        arr.append(x4[0][1])

    if(len(arr)!=4):
        return False
    else :
        sql = "INSERT INTO catatan (tanggal, matkul, jenis, topik) VALUES(%s,%s,%s,%s)"
        val = (arr[0],arr[1],arr[2],arr[3])
        curs.execute(sql,val)
        mysqldb.commit()
        return True

def printTask(query):
    if (query == "all"):
        sql = "SELECT * FROM catatan"
        curs.execute(sql)
        result = curs.fetchall()

        for data in result:
            print(data)
    elif (query == "today"):
        tgl = datetime.date(datetime.now())
        
        sql = "SELECT * FROM catatan WHERE jenis = %(tubes)s"
        curs.execute(sql, {'tubes':'tubes'})
        result = curs.fetchall()

        for data in result:
            print(data)
    else :
        print(type(query))
        print("wrong")
    
def deleteTask(in_id):
    sqlid = "SELECT id from catatan where id=%(id)s"
    curs.execute(sqlid,{'id' : in_id})
    result = curs.fetchall()
    if(len(result)!=0):
        sql = "DELETE FROM catatan WHERE id = %(id)s"
        curs.execute(sql, {'id':in_id})
        mysqldb.commit()
        return True
    else:
        return False

def updateTask(in_id, in_tanggal):
    month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    patt = '[0-9]{2}[/][0-9]{2}[/][0-9]{4}'
    patt2 = '[0-9]{2}[-][0-9]{2}[-][0-9]{4}'
    sqlid = "SELECT id from catatan where id=%(id)s"
    curs.execute(sqlid,{'id' : in_id})
    result = curs.fetchall()
    if(len(result)!=0):
        if(re.search(patt,in_tanggal)):
            tanggal = str(in_tanggal).split('/')
            tanggal_fix=(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
        elif(re.search(patt2,in_tanggal)):
            tanggal = str(in_tanggal).split('-')
            tanggal_fix=(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
        else:
            tanggal = str(in_tanggal).split()
            bulan = 0
            for i in range(12):
                if(tanggal[1]==month[i]):
                    bulan=i+1
                    if(bulan<10):
                        bulan = '0'+str(bulan)
                    else:
                        bulan = str(bulan)
            tanggal_fix=(tanggal[2]+'/'+bulan+'/'+tanggal[0])
        sqlupdate = 'UPDATE catatan SET tanggal = %s WHERE id = %s'
        val = (tanggal_fix,in_id)
        curs.execute(sqlupdate,val)
        mysqldb.commit()
        return True
    else:
        return False

def askDeadline(in_matkul):
    sql = "SELECT * FROM catatan WHERE matkul=%(matkul)s and (jenis='tubes' or jenis='tucil')"
    curs.execute(sql, {'matkul':in_matkul})
    result = curs.fetchall()

    for data in result:
        print(data)

#print(addTask(text))
# printTask(all)
#print(deleteTask(1))
#askDeadline('IF2230')


