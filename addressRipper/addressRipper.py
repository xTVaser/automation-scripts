import binascii

inputFile = open("ye.CEM", "rb")

loadPtr = '01251400'

def formattedHexString(hexString):
    hexString = str.capitalize(hexString)
    splitEveryByte = [hexString[i:i+2] for i in range(0, len(hexString), 2)]
    finalString = ""
    count = 0
    for byte in splitEveryByte:
        count += 1
        finalString += byte
        if count != 4:
            finalString += " "
    return finalString

try:
    prefixDWORD = inputFile.read(4)
    DWORD = inputFile.read(4)
    foundHeader = False
    EOFReached = False

    levelsNTSC = {}
    numBytesIterated = 8

    while DWORD != "" and EOFReached is not True:

        hexDWORD = binascii.hexlify(DWORD)
        hexPrefixDWORD = binascii.hexlify(prefixDWORD)

        #if numBytesIterated > 2120:
        #debug    print "ye"


        # If we have found the load ptr, then the previous byte we need to store
        if hexDWORD == loadPtr:
            # Now we need to search byte by byte for the text
            hexDWORD = binascii.hexlify(inputFile.read(4))
            numBytesIterated += 4
            constructHeader = ""
            foundChars = 0
            while hexDWORD != "":
                for byte in [hexDWORD[i:i+2] for i in range(0, len(hexDWORD), 2)]:
                    # if numBytesIterated > 2249:
                    #     print "YE!"
                    numBytesIterated += 1
                    ascii = int(byte, 16)
                    if (ascii >= 65 and ascii <= 122) or ascii == 45 or ascii == 46:
                        constructHeader += chr(ascii)
                        foundChars = foundChars + 1
                    else:
                        if foundChars >= 4:  # if we've found atleast 4 characters, then we've probably found the name and ended off
                            foundHeader = True
                            hexDWORD = ""
                            break
                        foundChars = 0  # otherwise, keep looking
                        constructHeader = ""
                if foundHeader is False:
                    hexDWORD = binascii.hexlify(inputFile.read(4))
            levelsNTSC[constructHeader] = formattedHexString(binascii.hexlify(prefixDWORD)) + " " + formattedHexString(binascii.hexlify(DWORD))
            foundHeader = False


        prefixDWORD = DWORD
        DWORD = inputFile.read(4)
        numBytesIterated += 4

    outputFile = open('outputaddrs.txt', 'w')
    for levelName in levelsNTSC.iterkeys():
        print >> outputFile, "%30s%30s" % (levelName, levelsNTSC[levelName])

finally:
    inputFile.close()




