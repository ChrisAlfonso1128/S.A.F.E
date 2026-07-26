import hashlib
import os

chunkSize: int = 65536 # 64KB

def calculateSHA256(filePath):

    SHA256HashVar = hashlib.sha256()

    with open(filePath, "rb") as file:

        while True:

            dataRead = file.read(chunkSize)

            if(dataRead == b""):

                break

            SHA256HashVar.update(dataRead)

        return SHA256HashVar.hexdigest()

def getHashOfDirectoryFiles(directoryPath):

    allHashes = {}

    for dirPath, dirName, dirFiles in os.walk(directoryPath):

        for file in dirFiles:

            filePath = os.path.join(dirPath, file)

            try:

                fileHash = calculateSHA256(filePath)

            except OSError as err:

                print(f"{filePath}'s SHA256 could not be calculated. ERROR: {err}")
                continue

            if(fileHash not in allHashes):

                allHashes[fileHash] = []

            allHashes[fileHash].append(filePath)

    return allHashes

if(__name__ == "__main__"):

    path = input("Input directory path to scan for duplicates: ").strip()
    hashData = getHashOfDirectoryFiles(path)
    noDuplicates = True

    for hashKey, listOfFiles in hashData.items():

        if(len(listOfFiles) > 1):

            noDuplicates = False

            print("\nDUPLICATE FILES DETECTED")
            print("===========================================")
            print("\n".join(str(filePath) for filePath in listOfFiles))

    if(noDuplicates):

        print(f"NO DUPLICATE FILES WERE FOUND IN THE SPECIFIED PATH AT: {path}")