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

#Pemanggilan query
status = False
query = input("Masukkan query : ")
keys = keywords.keys()
candidate_ques_ans = []
default = "Halo, ada yang bisa dibantu?"
if len(query) > 0:
    #Pre-processing query
    proc_query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))
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

        query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))
        words = query.split()
        sol = []
        for w in words:
            arr = levenshtein.rekomendasi(w, katasubs)
            if len(arr) != 0:
                for i in range(len(arr)):
                    sol.append(arr[i])
            
        if len(sol) != 0:
            print("Apakah maksud ada : ")
            for s in sol:
                print("-", s)
            status = True
            exit()

        if (updateTask(query) == True):
            status = True
            exit()
        elif (addTask(query) == True):
            status = True
            exit()
        elif (askDeadline(query) != None):
            status = True
            exit()
        elif (deleteTask(query) == True):
            status = True
            exit()

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
                printDeadline(result)
            elif (ans == "show-today-deadline"):
                result = printTask("today", None, None)
                printDeadline(result)
            elif (ans == "show-features"):
                print('''
                ~ Chatbot : SimSimi ~\n
                [Fitur]\n
                1. Menambahkan task baru\n
                2. Melihat daftar task yang harus dikerjakan\n
                3. Menampikan deadline dari suatu task tertentu\n
                4. Memperbarui task tertentu\n
                5. Menandai bahwa suatu task sudah selesai dikerjakan\n
                6. Menampilkan opsi help yang difasilitasi oleh assistant\n
                [Daftar Kata Penting]\n
                1. Kuis\n
                2. Ujian\n
                3. Tucil\n
                4. Tubes\n
                5. Praktikum\n''')
            elif (len(ans) > 0 and status == False):
                print(ans)
            else:
                pass

        else:
            result = []
            while(str(regex_query) != None or status == False):
                if (foundKeywords(regex_query)):
                    result = printTask("task", regex_query, None)
                    regex_query = delKeywords(regex_query, "task")
                    if len(result) == 0:
                        break
                else:
                    if (re.findall("bulan", regex_query)):
                        result = printTask("month", regex_query, result)
                    elif (re.findall("minggu", regex_query)):
                        result = printTask("week", regex_query, result)
                    elif (re.findall("hari", regex_query)):
                        result = printTask("day", regex_query, result)
                    else:
                        if (foundInterval(regex_query)):
                            result = printTask("interval", regex_query, result)
                            status = True
                        else:
                            result = printTask("date", regex_query, result)
                            status = True
                    regex_query = delKeywords(regex_query, "deadline")
                    regex_query = None

                if (regex_query == None or regex_query == "(.*)deadline(.*)"):
                    break

            if (len(result) == 0):
                print("Tidak ada data yang memenuhi")
            else:
                print("\n[Daftar Deadline]")
                printDeadline(result)

            '''else:
                print("Saya tidak mengerti")'''

    else:
        query = remove_nwhitespace(remove_stopwords(remove_noise(to_lowercase(query))))
        arr = rekomendasi(query, katasubs)

        if len(arr) == 0:
            print("Maaf, saya tidak mengerti")
        for i in range(len(arr)):
            print(arr[i])