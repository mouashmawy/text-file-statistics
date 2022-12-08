import string
import matplotlib.pyplot as plt
import numpy as np



class Stat:
    def __init__(self, filename:str):
        self.filename = filename

        self.textFileLength=0
        self.textInFile = ""
        self.sortedFreqList =[]
        # preparing letters lists
        # aAbBcC...012...789
        allLetersList = ""
        for i in range(len(string.ascii_lowercase)):
            allLetersList += string.ascii_lowercase[i] + string.ascii_uppercase[i]
        allLetersList += string.digits
        # preparing letters lists
        self.letterFreqDict = {}
        for letter in allLetersList:
            self.letterFreqDict[letter] = 0


    def __str__(self):
        return f"File name: {self.filename}"

    def __inputFile(self):
        # Reading text from file
        textFileName = self.filename
        try:
            file = open(textFileName, encoding='utf-8')
            self.textInFile = file.read().replace(" ", "")
            self.textFileLength = len(self.textInFile)
        finally:
            file.close()

    def calc(self):
        for letter in self.textInFile:
            self.letterFreqDict[letter] += 1
        self.sortedFreqList = sorted(self.letterFreqDict.items(), key=lambda kv: kv[1], reverse=1)

    def getHighest(self):
        try:
            numOfHighestFreqInput = 5  # int(input("Number of highest frequencies letters: "))
        except:
            print("not a number....")
            exit(0)
        for i in range(numOfHighestFreqInput):
            print(f"letter {self.sortedFreqList[i][0]}:: {self.sortedFreqList[i][1]}")



    def PMF(self):
        pass

    def CDF(self):
        pass

    def mean(self):
        pass

    def variance(self):
        pass













x_letters = np.array(list(letterFreqDict.keys()))
y_freq = np.array(list(letterFreqDict.values()))
print(x_letters)
# plt.bar(x_letters, y_freq)
# plt.show()
# plt.plot(x_letters, y_freq)
# plt.show()




#Generating PMF & CDF
x_numbers = np.array(list(range(10,len(x_letters)+10))) #Generating a list starting 10 for a rnage in length letter list
PMF = y_freq / textFileLength


CDF = PMF.copy()
for i in range(1, len(PMF)):
    CDF[i]= CDF[i] + CDF[i - 1]

plt.plot(x_letters, CDF)
# plt.show()

mean = np.sum(x_numbers * PMF)
print(mean)


variance = np.sum(x_numbers **2 * PMF) - mean**2
# variance2 = sum((x_numbers-mean)**2 * PMF)
print(np.sum(x_numbers*y_freq)/textFileLength)