#returns a string of the subkey permutation


import numpy as np


def SubkeyPermute(KEY, verbose):
    permuteKEY =[57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    output = []

    for i in range(0, len(permuteKEY)):
        output += KEY[int(permuteKEY[i]-1)]
    
    if(verbose):
        print("First Key Permutation Order : ")
        concatinatelisttoprint(output)
        print()

    
    return output

#permutes the subkey for each round
def finalSubkeyPermute(cx, dx, verbose, subkeynumber):
    key = cx + dx
    output = []
    permuteKey = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    
    for i in range(0, len(permuteKey)):
        output += key[int(permuteKey[i]-1)]
   
    if (verbose):
        print("\nSubkey number " + str(subkeynumber) + " is:")
        concatinatelisttoprint(output)
   
    return output

def initialFunctionPermutation(Plaintext, verbose):
    permuteKey = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
    output = []
    for i in range(0, len(permuteKey)):
        output += Plaintext[int(permuteKey[i]-1)]
    if (verbose):
        print("\nAfter the permutation, the text is:")
        concatinatelisttoprint(output)
    return output

#left shifts a list and shows verbose output
def listleftshift(list, verbose, side, shift):
    list = list[-shift:] + list[:-shift]

    if (verbose):
        if (side == "neither"):
            print("After left sifting, your output is:")
            concatinatelisttoprint(list)
        else:
            print("\nAfter left shifting, the "+side+" is:")
            concatinatelisttoprint(list)
    
    return list

#Calls the other functions for the DES block Cipher
def DESBlockCipher(Lx, Rx, subkey, verbose):
    global round
    if verbose:
        print("\n\nDES round "+str(round)+" begins!")
        print("R"+str(round-1)+" is:")
        concatinatelisttoprint(Rx)
        print("\nL"+str(round-1)+"is:")
        concatinatelisttoprint(Lx)
    
    output = ExpansionFunction(Rx, verbose)
    output = XORFunc(output, subkey, verbose, "the subkey")

    #perform The most complicated function
    output = transformPermutationSblock(output, verbose)
    
    output = afterSblockPermutation(output, verbose)

    #now begins the big Switch!
    oldRx = Rx
    Rx = XORFunc(Lx, output, verbose, "the left side")
    Lx = oldRx
    
    round += 1
    return Lx, Rx

#performs the intial permutation for the actual DES Cipher
def ExpansionFunction(Rx, verbose):
    permuteKey = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
    output = []
    for i in range(0, int(len(permuteKey))):
        output += Rx[int(permuteKey[i]-1)]
    
    if (verbose):
        print("\nThe permutation expansion output for round "+str(round)+" is:" )
        concatinatelisttoprint(output)
    
    return output

#Performs the XOR Function
def XORFunc(T1, T2, verbose, subject):
    #Actual XOR function
    output = []
    for i in range(0, len(T1)):
        if (T1[i] != T2[i]):
            output += '1'
        else:
            output += '0'
    
    if (verbose):
        print("\nThe output for an XOR with "+subject+" is:")
        concatinatelisttoprint(output)

    return output

#This is an odd function used to take the 48 bit key and turn it back into 32 bits
#It uses tables to shrinkthe bits. It's quite complitated
def transformPermutationSblock(Rx, verbose):
    #need to change the bits into 6 bit blocks
    #Creates the two lists of character combinations to permutate against the arrays
    
    segmentedxlist = []
    segmentedylist = []
    for i in range(0, 8):
        segmentedylist += Rx[i*6]
        segmentedylist[i] = segmentedylist[i] + Rx[(i*6)+5]
        
    for i in range(0, 8):
        segmentedxlist += Rx[(i*6)+1]
        segmentedxlist[i] = segmentedxlist[i] + Rx[(i*6)+2]
        segmentedxlist[i] = segmentedxlist[i] + Rx[(i*6)+3]
        segmentedxlist[i] = segmentedxlist[i] + Rx[(i*6)+4]
        
    verbPrintCheck("\nThe permutation for the y and x axis is:", verbose)
    verbPrintCheck(segmentedylist, verbose)
    verbPrintCheck(segmentedxlist, verbose)
    
    #Each block must then be turned into two binary numbrs
    
    segmentedxlistbinary = []
    segmentedylistbinary = []

    for i in segmentedxlist:
        segmentedxlistbinary.append((int(i, base=2)))
    
    for i in segmentedylist:
        segmentedylistbinary.append((int(i, base=2)))
        
    verbPrintCheck("Those numbers in decimal are:", verbose)
    verbPrintCheck(segmentedylistbinary, verbose)
    verbPrintCheck(segmentedxlistbinary, verbose)
    
    #Tables represent the permutation tables
    
    Table0 = ([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
               [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
               [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
               [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])
    
    Table1 = ([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
               [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
               [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
               [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])
    
    Table2 = ([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
               [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
               [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
               [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])
    
    Table3 = ([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
               [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
               [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
               [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])
    
    Table4 = ([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
               [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
               [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
               [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])
    
    Table5 = ([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
               [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
               [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
               [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])
    
    Table6 = ([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
               [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
               [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
               [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])
    
    Table7 = ([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
               [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
               [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
               [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

    #now begin doing the sblock permutation
    sBlockReturn = []
    
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 0, Table0))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 1, Table1))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 2, Table2))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 3, Table3))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 4, Table4))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 5, Table5))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 6, Table6))
    sBlockReturn.append(sblockFunc(segmentedylistbinary, segmentedxlistbinary, 7, Table7))
    
    #return the output back to a string and then make it an array
    output= []
    for i in sBlockReturn:
        output.append(str(bin(i)[2:].zfill(4)))
    output = ''.join(output)
    output = list(output)
    
    verbPrintCheck("Binary after the sblock permutation:", verbose)
    if verbose:
        concatinatelisttoprint(output)
    

    return output
    
    
    
#does the permutation and makes the rest of the Sblock function look cleaner
def sblockFunc(y, x, iteration, table):
    output = table[y[iteration]][x[iteration]]
    return output
    
def afterSblockPermutation(list, verbose):
    permuteKey = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
    output = []

    for i in range(0, len(permuteKey)):
        output += list[int(permuteKey[i]-1)]
    
    if(verbose):
        print("\nPermutation after the sBlock: ")
        concatinatelisttoprint(output)
    
    return output
    
def endingPermutation(list, verbose):
    permuteKey = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
    output = []
    for i in range(0, len(permuteKey)):
        output += list[int(permuteKey[i]-1)]
    
    if(verbose):
        print("\nThe result of the final permutation is: ")
        concatinatelisttoprint(output)
        print()
    
    return output
#returns the middle index for splitting and other functions
def middleIndexReturn(list):
    middle_index = len(list) // 2
    return middle_index

#returns the Key, but split into two variables
def listSplitter(KEY, verbose):
    middle_index = middleIndexReturn(KEY)
    LKey1 = KEY[:middle_index]
    RKey2 = KEY[middle_index:]

    if (verbose):
        print("The left half is:")
        concatinatelisttoprint(LKey1)
        print("\nThe right half is:")
        concatinatelisttoprint(RKey2)

    return [LKey1, RKey2]

#prints and concatinates a list
def concatinatelisttoprint(list):
    for i in range(0, len(list)):
        print(list[i], end='')

def verbPrintCheck(string, verbose):
    if (verbose):
        print(string)

def main():
    #Variable used to store the round of the Cipher
    global round
    round = 1
    #Begins the actual script
    KEY = input("Enter the KEY : ")
    PT = input("Enter the Plaintext")
    verbose = input("Enter a 1 or a 0 :")
    verbose = int(verbose)
    KEY = SubkeyPermute(KEY, verbose)

    #The Key is now permuted by splitting
    KEY = listSplitter(KEY, verbose)


    #Right and left are for the verbose output
    right = "right"
    left = "left"
    #This is the keys being shifted. C represents the left, while D represents the right
    #SK* means the subkey number
    #KEY will pass the variables
    #note:This could probably be simplified with a class or something. This code would go well with meatballs
    verbPrintCheck("", verbose)
    C1 = listleftshift(KEY[0], verbose, left, -1)
    D1 = listleftshift(KEY[1], verbose, right, -1)
    KEY[0] = C1
    KEY[1] = D1
    SK1 = finalSubkeyPermute(C1, D1, verbose, 1)

    verbPrintCheck("", verbose)
    C2 = listleftshift(KEY[0], verbose, left, -1)
    D2 = listleftshift(KEY[1], verbose, right, -1)
    KEY[0] = C2
    KEY[1] = D2
    SK2 = finalSubkeyPermute(C2, D2, verbose, 2)

    verbPrintCheck("", verbose)
    C3 = listleftshift(KEY[0], verbose, left, -2)
    D3 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C3
    KEY[1] = D3
    SK3 = finalSubkeyPermute(C3, D3, verbose, 3)

    verbPrintCheck("", verbose)
    C4 = listleftshift(KEY[0], verbose, left, -2)
    D4 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C4
    KEY[1] = D4
    SK4 = finalSubkeyPermute(C4, D4, verbose, 4)

    verbPrintCheck("", verbose)
    C5 = listleftshift(KEY[0], verbose, left, -2)
    D5 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C5
    KEY[1] = D5
    SK5 = finalSubkeyPermute(C5, D5, verbose, 5)

    verbPrintCheck("", verbose)
    C6 = listleftshift(KEY[0], verbose, left, -2)
    D6 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C6
    KEY[1] = D6
    SK6 = finalSubkeyPermute(C6, D6, verbose, 6)

    verbPrintCheck("", verbose)
    C7 = listleftshift(KEY[0], verbose, left, -2)
    D7 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C7
    KEY[1] = D7
    SK7 = finalSubkeyPermute(C7, D7, verbose, 7)

    verbPrintCheck("", verbose)
    C8 = listleftshift(KEY[0], verbose, left, -2)
    D8 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C8
    KEY[1] = D8
    SK8 = finalSubkeyPermute(C8, D8, verbose, 8)

    verbPrintCheck("", verbose)
    C9 = listleftshift(KEY[0], verbose, left, -1)
    D9 = listleftshift(KEY[1], verbose, right, -1)
    KEY[0] = C9
    KEY[1] = D9
    SK9 = finalSubkeyPermute(C9, D9, verbose, 9)

    verbPrintCheck("", verbose)
    C10 = listleftshift(KEY[0], verbose, left, -2)
    D10 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C10
    KEY[1] = D10
    SK10 = finalSubkeyPermute(C10, D10, verbose, 10)

    verbPrintCheck("", verbose)
    C11 = listleftshift(KEY[0], verbose, left, -2)
    D11 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C11
    KEY[1] = D11
    SK11 = finalSubkeyPermute(C11, D11, verbose, 11)

    verbPrintCheck("", verbose)
    C12 = listleftshift(KEY[0], verbose, left, -2)
    D12 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C12
    KEY[1] = D12
    SK12 = finalSubkeyPermute(C12, D12, verbose, 12)

    verbPrintCheck("", verbose)
    C13 = listleftshift(KEY[0], verbose, left, -2)
    D13 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C13
    KEY[1] = D13
    SK13 = finalSubkeyPermute(C13, D13, verbose, 13)

    verbPrintCheck("", verbose)
    C14 = listleftshift(KEY[0], verbose, left, -2)
    D14 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C14
    KEY[1] = D14
    SK14 = finalSubkeyPermute(C14, D14, verbose, 14)

    verbPrintCheck("", verbose)
    C15 = listleftshift(KEY[0], verbose, left, -2)
    D15 = listleftshift(KEY[1], verbose, right, -2)
    KEY[0] = C15
    KEY[1] = D15
    SK15 = finalSubkeyPermute(C15, D15, verbose, 15)

    verbPrintCheck("", verbose)
    C16 = listleftshift(KEY[0], verbose, left, -1)
    D16 = listleftshift(KEY[1], verbose, right, -1)
    KEY[0] = C16
    KEY[1] = D16
    SK16 = finalSubkeyPermute(C16, D16, verbose, 16)
    #Subkey Generation is now complete!

    #Now begins the Plaintext operations
    verbPrintCheck("\nnow begins the Actual Function for DES!\n", verbose)
    PT = initialFunctionPermutation(PT, verbose)
    verbPrintCheck("", verbose)
    PT = listSplitter(PT, verbose)

    #begin assinging Left and right variables
    #Lx means left, while Rx means right
    L0 = PT[0]
    R0 = PT[1]
    L1, R1 = DESBlockCipher(L0, R0, SK1,verbose)
    L2, R2 = DESBlockCipher(L1, R1, SK2,verbose)
    L3, R3 = DESBlockCipher(L2, R2, SK3,verbose)
    L4, R4 = DESBlockCipher(L3, R3, SK4,verbose)
    L5, R5 = DESBlockCipher(L4, R4, SK5,verbose)
    L6, R6 = DESBlockCipher(L5, R5, SK6,verbose)
    L7, R7 = DESBlockCipher(L6, R6, SK7,verbose)
    L8, R8 = DESBlockCipher(L7, R7, SK8,verbose)
    L9, R9 = DESBlockCipher(L8, R8, SK9,verbose)
    L10, R10 = DESBlockCipher(L9, R9, SK10,verbose)
    L11, R11 = DESBlockCipher(L10, R10, SK11,verbose)
    L12, R12 = DESBlockCipher(L11, R11, SK12,verbose)
    L13, R13 = DESBlockCipher(L12, R12, SK13,verbose)
    L14, R14 = DESBlockCipher(L13, R13, SK14,verbose)
    L15, R15 = DESBlockCipher(L14, R14, SK15,verbose)
    L16, R16 = DESBlockCipher(L15, R15, SK16,verbose)
    
    if verbose:
        print("\n\nL16 is")
        concatinatelisttoprint(L16)
        print("\nR16 is")
        concatinatelisttoprint(R16)
    
    #Final Reverse
    finalConcatination = R16+L16
    if verbose:
        print("\n\nThe final reverse is:")
        concatinatelisttoprint(finalConcatination)
    #final Permutation
    
    finaloutput = endingPermutation(finalConcatination, verbose)
    
    print("\nThe results are:")
    concatinatelisttoprint(finaloutput)
    
main()