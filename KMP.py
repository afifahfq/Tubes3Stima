def KMPSearch(pattern, txt):
    M = len(pattern)
    N = len(txt)

    lps = [0]*M # longest prefix suffix
    j = 0 # index pattern[]

    maks = 0
    count = 0

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pattern, M, lps)

    i = 0 # index txt[]
    while i < N:
        if pattern[j] == txt[i]:
            i += 1
            j += 1
            count += 1
            maks = max(count, maks)

        if j == M:
            j = lps[j-1]
            count = j
            #print ("Found pattern at index " + str(i-j))
            return (i-j)
        elif i < N and pattern[j] != txt[i]:
            if j != 0:
                j = lps[j-1]
                count = j
            else:
                i += 1
                count = 0
        
    return None

def computeLPSArray(pattern, M, lps):
    len = 0 # panjang prefix suffix terbesar sebelumnya

    lps[0] = 0 # inisialisasi lps[0] selalu 0
    i = 1

    # the loop hitung lps[i] dari i = 1 ke M-1
    while i < M :
        if pattern[i] == pattern[len] :
            len += 1
            lps[i] = len
            i += 1
        else :
            if len != 0:
                len = lps[len-1]
            else :
                lps[i] = 0
                i += 1

'''txt = "Siapa nama pembuat kode KMP?"
pattern1 = "pembuat"
pattern2 = "kamu"
result1 = KMPSearch(pattern1, txt)
print(result1)
result2 = KMPSearch(pattern2, txt)
print(result2)'''

# Modifikasi program KMP by Bhavya Jain