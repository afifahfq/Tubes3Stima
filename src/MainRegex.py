import re
from Sinonim import get_sinonim
from FileProcessing import *
from regex import *
import ReadFile
import itertools
import sys
from datetime import datetime
import levenshtein


#Baca file faq
Q, A = ReadFile.read_faq('pertanyaan.txt')
katasubs = ReadFile.read_txt('katasubs.txt')

#Pre-processing tiap pertanyaan
proc_Q = [remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(question)))) for question in Q]

#Bentuk dictionary dengan key-nya sebuah string dan valuenya merupakan indeks dari pertanyaan
#atau jawaban yang mengandung kata tersebut, (keyword akan dibutuhkan saat regex(?))
keywords = {}

botmsg = ""

def getBotArrivalMessage():
    return "Halo, ada yang bisa dibantu?"


#Mengisi dictionary keywords
indeks = 0
for question in proc_Q:
    words = get_words(question)

    for word in words:
        wordExist = False
        sinonimExist = False

        if word not in keywords:
            list_sinonim = get_sinonim(word)
            for sinonim in list_sinonim:
                if sinonim in keywords:
                    sinonimExist = True
                    break
        else:
            wordExist = True

        if not (wordExist or sinonimExist):
            keywords[word] = [indeks]
        elif sinonimExist:
            keywords[sinonim] += [indeks] 
        elif wordExist:
            keywords[word] += [indeks]

    indeks += 1

def changeEndline(strin):
    result = ""
    for i in range(len(strin)):
        if(strin[i] == "\n"):
            if(i < len(strin)-1):
                result = result + "<br>"
        else :
            result = result + strin[i]
    return result
        
def printDeadline(result):
    i = 1
    ret = ""
    for data in result:
        ret = ret + str(i) + ". " + " "
        ret = ret + "(ID: "+ str(data[0]) + ")" + " "
        ret = ret + str(data[1]) + " "
        ret = ret + "-" + str(data[2].upper()) + " "
        ret = ret + "-" + str(data[3].capitalize()) + " "
        ret = ret + "-" + str(data[4].capitalize()) + "\n"
        i += 1
    return ret

def getBotMessage(userMessage):
    #Pemanggilan query
    status = False
    queryasli = userMessage
    keys = keywords.keys()
    candidate_ques_ans = []
    default = "Halo, ada yang bisa dibantu?"
    botmsg = ""
    if len(queryasli) > 0:
        #Pre-processing query
        proc_query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(queryasli))))
        proc_query = remove_stopwords(proc_query)

        if (len(proc_query)>0):
            #Simpan seluruh sinonim dari tiap kata di query dan kata di query tsb
            query_words = get_words(proc_query)
            synonyms_word = [get_sinonim(word) for word in query_words]
            for i in range(len(query_words)):
                synonyms_word[i] += [query_words[i]]
            
            #Buat sebuah kombinasi kata dari synonnyms_word
            new_word_list = list(itertools.product(*synonyms_word))
            for words_list in new_word_list:
                #regex
                regex_query = "(.*)"
                match_words = ""
                indeks = -1
                len_query = len(" ".join(words_list))
                for w in words_list:
                    regex_query = regex_query + w + "(.*)"
                for q in proc_Q:
                    indeks = indeks + 1
                    match_words = re.match(regex_query,q)
                    len_question = 0
                    presentase = 0
                    if (match_words!=None):
                        len_question = len(q)
                        presentase = len_query/len_question
                        if (presentase>=0.30):
                            candidate_ques_ans.append((q,A[indeks],presentase))
            
            #print(regex_query)
            #print(candidate_ques_ans)

            query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(queryasli))))
            words = query.split()
            sol = []
            for w in words:
                arr = levenshtein.rekomendasi(w, katasubs)
                if len(arr) != 0:
                    for i in range(len(arr)):
                        sol.append(arr[i])
                
            if len(sol) != 0:
                botmsg = botmsg + "Apakah maksud ada : \n"
                for s in sol:
                    botmsg = botmsg + "-" + s + "\n"
                status = True
                return changeEndline(botmsg)

            if (updateTask(query) == True):
                status = True
                botmsg= botmsg + "Data task berhasil diperbaharui!\n"
                return changeEndline(botmsg)
            elif (checkAddTask(queryasli) != None):
                status = True
                result = addTask(queryasli)
                botmsg = botmsg + "[TASK BERHASIL DICATAT]\n"
                botmsg = botmsg + printDeadline(result)
                return changeEndline(botmsg)
            elif (askDeadline(query) != None):
                status = True
                result = askDeadline(query)
                for data in result:
                    tanggal = str(data[1])
                    print(tanggal.replace("-","/"))
                    botmsg = botmsg + str(data[1].strftime("%Y/%m/%d")) + "\n"
                return changeEndline(botmsg)
            elif (deleteTask(query) == True):
                status = True
                botmsg = botmsg + "Task berhasil dihapus!\n"
                return changeEndline(botmsg)

            elif (len(candidate_ques_ans)>0 and status == False):
                high_ans = []     
                low_ans = []
                ans = ""
                for a in candidate_ques_ans:
                    if a[2]>0.80:
                        high_ans.append(a)
                    else:
                        low_ans.append(a)

                if (len(high_ans)>0):
                    max = high_ans[0][2]
                    i = 0
                    indeks_max = 0
                    for ans in high_ans:
                        if (ans[2]>max):
                            indeks_max = i
                            max = ans[2]
                        i += 1
                    ans = high_ans[indeks_max][1]
                else:
                    ans = "Apa maksud anda : \n"
                    for q in low_ans:
                        ans += "-" + q[0] + "\n"

                if (ans == "show-all-deadline"):
                    result = printTask("all", None, None)
                    botmsg = botmsg + printDeadline(result)
                elif (ans == "show-today-deadline"):
                    result = printTask("today", None, None)
                    botmsg = botmsg + printDeadline(result)
                elif (ans == "show-features"):
                    botmsg = botmsg + "~ Chatbot : SimSimi ~\n"
                    botmsg = botmsg + "[Fitur]\n"
                    botmsg = botmsg + "1. Menambahkan task baru\n"
                    botmsg = botmsg + "2. Melihat daftar task yang harus dikerjakan\n"
                    botmsg = botmsg + "3. Menampikan deadline dari suatu task tertentu\n"
                    botmsg = botmsg + "4. Memperbarui task tertentu\n"
                    botmsg = botmsg + "5. Menandai bahwa suatu task sudah selesai dikerjakan\n"
                    botmsg = botmsg + "6. Menampilkan opsi help yang difasilitasi oleh assistant\n"
                    botmsg = botmsg + "[Daftar Kata Penting]\n"
                    botmsg = botmsg + "1. Kuis\n"
                    botmsg = botmsg + "2. Ujian\n"
                    botmsg = botmsg + "3. Tucil\n"
                    botmsg = botmsg + "4. Tubes\n"
                    botmsg = botmsg + "5. Praktikum\n"
                elif (len(ans) > 0 and status == False):
                    botmsg = botmsg + ans
                else:
                    pass

            else:
                result = []
                while(str(regex_query) != None or status == False):
                    if (foundKeywords(regex_query)):
                        status = True
                        result = printTask("task", regex_query, None)
                        regex_query = delKeywords(regex_query, "task")
                        if len(result) == 0:
                            break
                    else:
                        if (re.findall("bulan", regex_query)):
                            status = True
                            result = printTask("month", regex_query, result)
                        elif (re.findall("minggu", regex_query)):
                            status = True
                            result = printTask("week", regex_query, result)
                        elif (re.findall("hari", regex_query)):
                            status = True
                            result = printTask("day", regex_query, result)
                        elif (re.findall("task", regex_query) or re.findall("deadline", regex_query) or re.findall("tugas", regex_query)):
                            if (foundInterval(regex_query)):
                                result = printTask("interval", regex_query, result)
                                status = True
                            else:
                                result = printTask("date", regex_query, result)
                                status = True
                        else:
                            print("Saya tidak mengerti")
                        regex_query = delKeywords(regex_query, "deadline")
                        regex_query = None

                    if (regex_query == None or regex_query == "(.*)deadline(.*)"):
                        break

                if (len(result) == 0 and status == True):
                    botmsg = botmsg + "Tidak ada data yang memenuhi\n"
                elif (status == True):
                    botmsg = botmsg + "\n[Daftar Deadline]\n"
                    botmsg = botmsg + printDeadline(result)

        else:
            query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))
            arr = levenshtein.rekomendasi(query, katasubs)

            if len(arr) == 0:
                botmsg = botmsg +"Maaf, saya tidak mengerti\n"
            for i in range(len(arr)):
                botmsg = botmsg + arr[i] + "\n"
            botmsg = botmsg[:len(botmsg)-1]
    if(botmsg == ""):
        botmsg = default
    return changeEndline(botmsg)


print(getBotMessage("apa saja fitur yang ada"))