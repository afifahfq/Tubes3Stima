import json

#Baca file FAQ
def read_faq(filename):
    questions = []
    answers = []

    try:
        faq = open(filename, "r")
        lines = faq.readlines()
        faq.close()

        for line in lines:
            awal, akhir = 0, 0
            while (ord(line[awal]) != 46):
                awal += 1

            while (ord(line[akhir]) != 63):
                akhir += 1

            questions.append(line[awal+2:akhir])
            answers.append(line[akhir+2:-1])
            
    except FileNotFoundError:
        print("[ERROR] : File tidak ditemukan!")

    return questions, answers

#Baca sebuah file .txt
def read_txt(filename):
    hasil = []

    try:
        txtFile = open(filename, "r")
        lines = txtFile.readlines()
        txtFile.close()
        
        for line in lines:
            hasil.append(line[:-1])

    except FileNotFoundError:
        print("[ERROR] : File tidak ditemukan!")
    
    return hasil

#Baca sebuah file .json
def read_json(filename):
    try:
        jsonFile = open(filename)
        data = json.load(jsonFile)
        return data
    except FileNotFoundError:
        print("[ERROR] : File tidak ditemukan!")
        return None