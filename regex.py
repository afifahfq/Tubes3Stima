import re
from time import process_time
import mysql.connector
from datetime import datetime, timedelta
import FileProcessing

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
        result = curs.fetchall()
        print(result)

        sql = "SELECT * FROM catatan WHERE tanggal = %(tgl)s AND matkul = %(mtk)s AND jenis = %(jns)s AND topik = %(tpk)s"
        curs.execute(sql, {'tgl':arr[0], 'mtk':arr[1], 'jns':arr[2], 'tpk':arr[3]})
        result = curs.fetchall()

        print("[TASK BERHASIL DICATAT]")
        printDeadline(result)

        return True

def printTask(query, arg, result):
    if (query == "all"):
        sql = "SELECT * FROM catatan"
        curs.execute(sql)
        result = curs.fetchall()

        return result
    elif (query == "today"):
        currtgl = datetime.date(datetime.now())
        
        sql = "SELECT * FROM catatan WHERE tanggal = %(tgl)s"
        curs.execute(sql, {'tgl':currtgl})
        result = curs.fetchall()

        return result
    elif (query == "date"):
        arg = arg[12:]
        arg = arg.replace("(.*)", " ")

        currtgl = convertStrtoDate(arg)
        
        sql = "SELECT * FROM catatan WHERE tanggal = %(tgl)s"
        curs.execute(sql, {'tgl':currtgl})
        result = curs.fetchall()

        return result
    elif (query == "interval"):
        arg = arg[12:]
        arg = arg.replace("(.*)", " ")
        arg = arg.split("sampai")

        date1 = convertStrtoDate(arg[0])
        date1 = date1.replace("/", "-")
        date2 = convertStrtoDate(arg[1])
        date2 = date2.replace("/", "-")

        sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
        curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
        result = curs.fetchall()

        return result
    elif (query == "month"):
        arg = arg[12:]
        arg = arg.replace("(.*)", "")

        if (re.findall("depan", arg)):
            count = int(arg[arg.find("bulan") - 1])

            date1 = datetime.date(datetime.now())
            date2 = date1.replace(month=date1.month + 1)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
            result = curs.fetchall()

            return result
        elif (re.findall("belakang", arg)):
            count = int(arg[arg.find("bulan") - 1])

            date1 = datetime.date(datetime.now())
            date2 = date1.replace(month=date1.month - 1)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date2, 'tgl2':date1})
            result = curs.fetchall()

            return result
    elif (query == "week"):
        arg = arg[12:]
        arg = arg.replace("(.*)", "")

        if (re.findall("depan", arg)):
            count = int(arg[arg.find("minggu") - 1])

            date1 = datetime.date(datetime.now())
            date2 = datetime.date(datetime.now()) + timedelta(days = count * 7)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
            result = curs.fetchall()

            return result
        elif (re.findall("belakang", arg)):
            count = int(arg[arg.find("minggu") - 1])

            date2 = datetime.date(datetime.now())
            date1 = datetime.date(datetime.now()) - timedelta(days = count * 7)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
            result = curs.fetchall()

            return result
    elif (query == "day"):
        arg = arg[12:]
        arg = arg.replace("(.*)", "")

        if (re.findall("depan", arg)):
            count = int(arg[arg.find("hari") - 1])

            date1 = datetime.date(datetime.now())
            date2 = datetime.date(datetime.now()) + timedelta(days = count)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
            result = curs.fetchall()

            return result
        elif (re.findall("belakang", arg)):
            count = int(arg[arg.find("hari") - 1])

            date2 = datetime.date(datetime.now())
            date1 = datetime.date(datetime.now()) - timedelta(days = count)

            sql = "SELECT * FROM catatan WHERE tanggal BETWEEN CAST(%(tgl1)s AS DATE) AND CAST(%(tgl2)s AS DATE)"
            curs.execute(sql, {'tgl1':date1, 'tgl2':date2})
            result = curs.fetchall()

            return result
    elif (query == "task"):
        arg = arg[12:]
        arg = arg.replace("(.*)", "")
        
        keywords = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
        for k in keywords:
            if (k in arg):
                jenis = k
                break

        sql = "SELECT * FROM catatan WHERE jenis = %(jns)s"
        curs.execute(sql, {'jns':jenis})
        result = curs.fetchall()

        return result
    '''else :
        print("[ERROR] Wrong query") '''
    
def deleteTask(query):
    keywords = ["sudah", "selesai", "hapus"]
    for k in keywords:
        if (re.findall(k,query)):
            words = query.split()

            for w in words:
                if (re.findall('[0-9]{1}|[0-9]{2}', w)):
                    in_id = w
                    break

            sqlid = "SELECT id from catatan where id=%(id)s"
            curs.execute(sqlid,{'id' : in_id})
            result = curs.fetchall()

            if (len(result) == 0):
                print("Tidak ada data yang sesuai")
            else:
                sql = "DELETE FROM catatan WHERE id = %(id)s"
                curs.execute(sql, {'id':in_id})
                mysqldb.commit()
                return True
                
            return True
    return False

def updateTask(query):
    keywords = ["dirubah", "diubah", "ubah", "berubah", "menjadi", "diundur", "undur", "dimajukan", "maju", "delay"]
    for k in keywords:
        if (re.findall(k,query)):
            words = query.split()

            batas = ["ke", "menjadi", "jadi"]
            for b in batas:
                if (words.index(b) != -1):
                    indeks = words.index(b) + 1
                    tgl = words[indeks:]
                    tanggal = ' '.join([elem for elem in tgl])
                    str_tgl = convertStrtoDate(tanggal)
                    break

            new = [x for x in words if x not in tgl]
            for n in new:
                if (re.findall('[0-9]{1}|[0-9]{2}', n)):
                    in_id = n

            sqlupdate = 'UPDATE catatan SET tanggal = %s WHERE id = %s'
            val = (str_tgl,in_id)
            curs.execute(sqlupdate,val)
            mysqldb.commit()

            return True
            
    return False

def askDeadline(query):
    keywords = ["kapan", "kapankah"]
    for k in keywords:
        if (re.findall(k,query)):
            re_matkul = '([a-zA-Z]{2}[0-9]{4})'
            matkul = re.findall(re_matkul,query)

            re_jenis = 'tucil|tubes'
            jenis = re.findall(re_jenis,query)

            sql = "SELECT * FROM catatan WHERE matkul=%(mtk)s and jenis=%(jns)s"
            curs.execute(sql, {'mtk':matkul[0], 'jns':jenis[0]})
            result = curs.fetchall()

            if len(result) == 0:
                print("Tidak ada data yang sesuai")

            for data in result:
                print(data[1].strftime("%Y/%m/%d"))

            return True
        else:
            return None

def convertStrtoDate(str_tgl):
    month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    patt = '[0-9]{2}[/][0-9]{2}[/][0-9]{4}'
    patt2 = '[0-9]{2}[-][0-9]{2}[-][0-9]{4}'

    if(re.search(patt,str_tgl)):
        tanggal = str(str_tgl.split('/'))
        tanggal_fix=(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
    elif(re.search(patt2,str_tgl)):
        tanggal = str(str_tgl).split('-')
        tanggal_fix=(tanggal[2]+'/'+tanggal[1]+'/'+tanggal[0])
    else:
        tanggal = str(str_tgl).split()
        bulan = 0
        for i in range(12):
            if(tanggal[1]==month[i]):
                bulan=i+1
                if(bulan<10):
                    bulan = '0'+str(bulan)
                else:
                    bulan = str(bulan)
        tanggal_fix=(tanggal[2]+'/'+bulan+'/'+tanggal[0])

    return(tanggal_fix)

def foundKeywords(query):
    keywords = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
    for k in keywords:
        if (k in query):
            return True
    return False

def delKeywords(query, currkey):
    keywords = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
    
    if (currkey == "deadline") and (re.findall(currkey, query)):
        query = query.replace("(.*)deadline", "")
        return query
    elif (currkey == "task"):
        for k in keywords:
            if (re.findall(k, query)):
                query = query.replace("(.*)%s" %k, "")
                return query
    else:
        return None

def foundInterval(query):
    month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    re_tgl = '[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}'

    tglcheck = re.findall(re_tgl,query)
    if len(tglcheck) >= 2 :
        return True

    ycheck = re.findall('[0-9]{4}',query)
    if len(ycheck) >=2:
        return True

    mcount = 0
    for m in month:
        if (m in query):
            mcount += 1
    if mcount >= 2:
        return True

    query = query.replace(ycheck[0], "")
    dcheck = re.findall('[0-9]{2}',query)
    if len(dcheck) >=2:
        return True
    
    return False

def printDeadline(result):
    i = 1
    for data in result:
        print(i, ". ", end=" ")
        print("(ID: %d)" %data[0], end=" ")
        print(data[1].strftime("%Y/%m/%d"), end=" ")
        print("-", data[2].upper(), end=" ")
        print("-", data[3].capitalize(), end=" ")
        print("-", data[4].capitalize())
        i += 1

#print(addTask(text))
# printTask(all)
#print(deleteTask(1))
#askDeadline('IF2230')


