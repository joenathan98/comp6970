import sys, string


s1 = "SRCTHLENRDFVTGTQGTTRVTLVLELGGCVTITAEGKPSMDVWLDAIYQENPAKTREYCLHAKLSDTKVAARCPTMGPATLAEEHQGGTVCKRDQSDRGWGNHCGLFGKGSIVACVKAACEAKKKATGHVYDANKIVYTVKVEPHTGDYVAANETHSGRKTASFTISSEKTILTMGEYGDVSLLCRVASGVDLAQTVILELDKTVEHLPTAWQVHRDWFNDLALPWKHEGAQNWNNAERLVEFGAPHAVKMDVYNLGDQTGVLLKALAGVPVAHIEGTKYHLKSGHVTCEVGLEKLKMKGLTYTMCDKTKFTWKRAPTDSGHDTVVMEVTFSGTKPCRIPVRAVAHGSPDVNVAMLITPNPTIENNGGGFIEMQLPPGDNIIYVGELSHQWFQK"
s2 = "IRCIGVSNRDFVEGMSGGTWVDVVLEHGGCVTVMAQDKPTVDIELVTTTVSNMAEVRSYCYEASISDMASDSRCPTQGEAYLDKQSDTQYVCKRTLVDRGWGNGCGLFGKGSLVTCAKFACSKKMTGKSIQPENLEYRIMLSVHGSQHSGMIVNDTGHETDENRAKVEITPNSPRAEATLGGFGSLGLDCEPRTGLDFSDLYYLTMNNKHWLVHKEWFHDIPLPWHAGADTGTPHWNNKEALVEFKDAHAKRQTVVVLGSQEGAVHTALAGALEAEMDGAKGRLSSGHLKCRLKMDKLRLKGVSYSLCTAAFTFTKIPAETLHGTVTVEVQYAGTDGPCKVPAQMAVDMQTLTPVGRLITANPVITESTENSKMMLELDPPFGDSYIVIGVGEKKITHHWHRSGSTIGKAFEATVRGAKRMAVLGDTAWDFGSVGGALNSLGKGIHQIFGAAFKSLFGGMSWFSQILIGTLLMWLGLNTKNGSISLMCLALGGVLIFLSTAVSA"


fi = open("blosum62.txt", "r")
content = fi.readlines()
blosum62 = []

'''
Populates BLOSUM62 matrix with text file input
'''
for i in content:
    blosum62.append(i.strip("\n"))
fi.close()

'''
Splits input into string matrix
'''
finalBlosum = []
for i in blosum62:
    finalBlosum.append(i.split(' '))

'''
removes excess spaces from array
'''

for row in finalBlosum:
    for elem in row:
        if elem == '':
            row.remove('')

for elem in finalBlosum[0]:
    if elem == '':
        finalBlosum[0].remove('')

finalBlosum[0].insert(0, ' ')




def createMatrix(string1, string2):
    n = len(string1) + 1
    m = len(string2) + 1

    a = [0] * n
    for i in range(n):
        a[i] = [0] * m

    num = 0
    for i in range(n):
        a[i][0] = num
        num -= 1

    num = 0
    for i in range(m):
        a[0][i] = num
        num -= 1

    return a

def createSmithMatrix(string1, string2):
    n = len(string1) + 1
    m = len(string2) + 1

    a = [0] * n
    for i in range(n):
        a[i] = [0] * m

    return a


def matchNeedleman(l1, l2, finalBlosum):
    l1Index = finalBlosum[0].index(l1)
    l2Index = 0

    for i, row in enumerate(finalBlosum):
        if row[0] == l2:
            l2Index = i
            break

    if l1 == l2:
        return int(finalBlosum[l1Index][l2Index])
    elif l1 == "_" or l2 == "_":
        return int(finalBlosum[l1Index][l2Index])
    else:
        return int(finalBlosum[l1Index][l2Index])

def needlman_wunsch(string1, string2, mat):
    n = len(string1)
    m = len(string2)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = mat[i-1][j-1] + matchNeedleman(string1[i-1],string2[j-1], finalBlosum)
            top = mat[i][j-1] + matchNeedleman("*", string2[j-1], finalBlosum)
            side = mat[i-1][j] + matchNeedleman(string1[i-1], "*", finalBlosum)
            mat[i][j] = max(diag, top, side)

    
    alignment1 = []
    bufferAlign = []
    alignment2 = []

    score = mat[n][m]

    while n > 0 and m > 0 :

        currentVal = mat[n][m]
        diagVal = mat[n-1][m-1]
        leftVal = mat[n][m-1]

        if currentVal == diagVal + matchNeedleman(string1[n-1],string2[m-1], finalBlosum):
            alignment1.append(string1[n-1])
            if string1[n-1] == string2[m-1]:
                bufferAlign.append("|")
            else:
                bufferAlign.append("*")
            alignment2.append(string2[m-1])
            n -= 1
            m -= 1

        elif currentVal == leftVal + matchNeedleman(string1[i-1], "*", finalBlosum):
            alignment2.append("-")
            bufferAlign.append(" ")
            alignment1.append(string2[m-1])
            m -= 1

        else:
            alignment1.append(string1[n-1])
            bufferAlign.append("*")
            alignment2.append("-")
            n -= 1
    
    while n > 0:
        alignment1.append(string1[n-1])
        bufferAlign.append(" ")
        alignment2.append("-")
        n -= 1

    while m > 0:
        alignment2.append(string2[m-1])
        bufferAlign.append(" ")
        alignment1.append("-")
        m -= 1

    

    alignment1.reverse()
    bufferAlign.reverse()
    alignment2.reverse()

    concat_aligment1 = ''.join(map(str, alignment1[0:]))
    concat_buffer = ''. join(map(str, bufferAlign[0:]))
    concat_aligment2 = ''.join(map(str, alignment2[0:]))

    n = 80
    
    formatArray1 = [concat_aligment1[i:i+n] for i in range(0, len(alignment1), n)]
    formatBuffer = [concat_buffer[i:i+n] for i in range(0, len(alignment2), n)]
    formatArray2 = [concat_aligment2[i:i+n] for i in range(0, len(alignment2), n)]

    print("NEEDLEMAN")
    print('\n')
    print("SCORE: ", score)
    print('\n')

    for i in range(len(formatArray1)):
        print(formatArray1[i])
        print(formatBuffer[i])
        print(formatArray2[i])
        print("\n")



def smith_waterman(string1, string2, mat):
    n = len(string1)
    m = len(string2)
    maximum = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = mat[i-1][j-1] + matchNeedleman(string1[i-1],string2[j-1], finalBlosum)
            top = mat[i][j-1] +  matchNeedleman("*", string2[j-1], finalBlosum)
            side = mat[i-1][j] + matchNeedleman(string1[i-1], "*", finalBlosum)
            mat[i][j] = max(diag, top, side, 0)

            if mat[i][j] > maximum:
                maximum = mat[i][j]
                x = i
                y = j

    score = maximum
    alignment1 = []
    bufferAlign = []
    alignment2 = []


    while x > 0 and y > 0 and mat[x][y] != 0:

        currentVal = mat[x][y]
        diagVal = mat[x-1][y-1]
        leftVal = mat[x][y-1]

        if currentVal == diagVal + matchNeedleman(string1[x-1],string2[y-1], finalBlosum):
            alignment1.append(string1[x-1])
            if string1[x-1] == string2[y-1]:
                bufferAlign.append("|")
            else:
                bufferAlign.append("*")
            alignment2.append(string2[y-1])
            x -= 1
            y -= 1

        elif currentVal == leftVal + matchNeedleman(string1[x-1], "*", finalBlosum):
            alignment2.append("-")
            bufferAlign.append(" ")
            alignment1.append(string2[y-1])
            y -= 1

        else:
            alignment1.append(string1[x-1])
            bufferAlign.append("*")
            alignment2.append("-")
            x -= 1
    
    

    alignment1.reverse()
    bufferAlign.reverse()
    alignment2.reverse()

    concat_aligment1 = ''.join(map(str, alignment1[0:]))
    concat_buffer = ''. join(map(str, bufferAlign[0:]))
    concat_aligment2 = ''.join(map(str, alignment2[0:]))

    n = 80
    
    formatArray1 = [concat_aligment1[i:i+n] for i in range(0, len(alignment1), n)]
    formatBuffer = [concat_buffer[i:i+n] for i in range(0, len(alignment2), n)]
    formatArray2 = [concat_aligment2[i:i+n] for i in range(0, len(alignment2), n)]

    print("SMITH")
    print('\n')
    print("SCORE: ", score)
    print('\n')

    for i in range(len(formatArray1)):
        print(formatArray1[i])
        print(formatBuffer[i])
        print(formatArray2[i])
        print("\n")




    
needleMatrix = createMatrix(s1, s2)
needlman_wunsch(s1, s2, needleMatrix)

smithMatrix = createSmithMatrix(s1, s2)
smith_waterman(s1, s2, smithMatrix)

            
        

