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

#prints and concatinates a list
def concatinatelisttoprint(list):
    for i in range(0, len(list)):
        print(list[i], end='')

def main():
    #Begins the XOR function calls
    S1 = input("Input 1 : ")
    S2 = input("Input 2 : ")

    L1 = []
    L2 = []

    for i in S1:
        L1.append(i)
    
    for i in S2:
        L2.append(i)

    XORoutput = XORFunc(L1, L2, 0, "")

    print()
    concatinatelisttoprint(XORoutput)

main()
