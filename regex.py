import re
#import mysql.connector


#text = "Halo tolong dicatat ya matkul IF2230 ada tubes materi string matching 05 april 2021"

def isDetected(text):
    arr = []
    month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    re_matkul = '[a-zA-Z]{2}[0-9]{4}'
    re_jenis = 'kuis|tucil|tubes|ujian|praktikum|rangkuman'
    re_tgl = '[0-9]{2}[/-]?\s?\w+[/-]?\s?[0-9]{4}'
    re_materi = '(materi |tentang |mengenai )+(.*)'
    x1 = re.findall(re_matkul,text)
    if(x1):
        arr.append(x1[0])
        text=text.replace(x1[0],"")

    x2 = re.findall(re_jenis,text)
    if(x2):
        arr.append(x2[0])
        text=text.replace(x2[0],"")

    x3 = re.findall(re_tgl,text)
    if(x3):
        patt = '[0-9]{2}[/-][0-9]{2}[/-][0-9]{4}'
        if(re.search(patt,text)):
            arr.append(x3[0])
            text=text.replace(x3[0],"")
        else:
            tanggal = str(x3[0]).split()
            bulan = 0
            for i in range(12):
                if(tanggal[1]==month[i]):
                    bulan=i+1
                    if(bulan<10):
                        bulan = '0'+str(bulan)
                    else:
                        bulan = str(bulan)
            arr.append(tanggal[0]+'/'+bulan+'/'+tanggal[2])
            text=text.replace(x3[0],"")

    x4 = re.findall(re_materi,text)
    if(x4):
        arr.append(x4[0][1])

    if(len(arr)!=4):
        return False
    else :
        # mau dimasukin database
        return True

#print(isDetected(text))




