def badCharHeuristic(string, size):
    # Inisialisasi
    badChar = [-1]*256
 
    for i in range(size):
        badChar[ord(string[i])] = i

    return badChar
 
def search(txt, pattern):
    m = len(pattern)
    n = len(txt)

    badChar = badCharHeuristic(pattern, m)
 
    # s adalah shift dari pattern terhadap txt
    s = 0
    while(s <= n-m):
        j = m-1

        while j>=0 and pattern[j] == txt[s+j]:
            j -= 1
 
        if j<0:
            print("Pattern occur at shift = {}".format(s))
 
            # shift pattern : next char di txt sejajar dgn last occurence di pattern
            s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
        else:
            # shift pattern : bad char di txt sejajar dgn last occurence di pattern
            s += max(1, j-badChar[ord(txt[s+j])])
 
 
def main():
    txt = "Siapa nama pembuat kode BM?"
    pat = "nama"
    search(txt, pat)
 
if __name__ == '__main__':
    main()
 
# Modifikasi program BM by Atul Kumar