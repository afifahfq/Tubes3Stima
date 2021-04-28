import ReadFile

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    elif len(s2) == 0:
        return len(s1)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        temp_row = [i + 1]
        for j, c2 in enumerate(s2):
            insert = prev_row[j + 1] + 1
            delete = temp_row[j] + 1       
            subs = prev_row[j] + (c1 != c2)
            temp_row.append(min(insert, delete, subs))
        prev_row = temp_row
    
    return prev_row[-1]

def bobotleven(kata1, kata2):
    dist = levenshtein(kata1,kata2)
    maks = max(len(kata1),len(kata2))
    bobot = (1-(dist/maks))
    return bobot


def rekomendasi(in_kata, hasil):
    rekomen = []
    for i in range(len(hasil)):
        if(bobotleven(in_kata,hasil[i])>0.75):
            rekomen.append(hasil[i])
    return rekomen

# hasil=ReadFile.read_txt('katasubs.txt')
# arr=rekomendasi('dedline',hasil)
# for i in range(len(arr)):
#     print(arr[i])