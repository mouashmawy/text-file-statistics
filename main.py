import string
import matplotlib.pyplot as plt
import numpy as np



class Stat:
    def __init__(self, filename:str):
        self.filename = filename

        self.textFileLength=0
        self.textInFile = ""
        self.sortedFreqList =[]

        self.x_letters = None
        self.y_freq = None
        self.y_PMF = None
        self.y_CDF = None

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

        # Reading text from file
        textFileName = self.filename
        try:
            file = open(textFileName, encoding='utf-8')
            self.textInFile = file.read().replace(" ", "")
            self.textFileLength = len(self.textInFile)
        finally:
            file.close()


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

        self.x_letters = np.array(list(self.letterFreqDict.keys()))
        self.y_freq = np.array(list(self.letterFreqDict.values()))

        # Generating PMF
        self.x_numbers = np.array(list(
            range(10, len(self.x_letters) + 10)))  # Generating a list starting 10 for a rnage in length letter list
        self.y_PMF = self.y_freq / self.textFileLength
        # Generating CDF
        self.y_CDF = self.y_PMF.copy()
        for i in range(1, len(self.y_PMF)):
            self.y_CDF[i] = self.y_CDF[i] + self.y_CDF[i - 1]



    def freqPlot(self):
        plt.bar(self.x_letters, self.y_freq)
        plt.show()
        plt.plot(self.x_letters, self.y_freq)
        plt.show()
        pass


    def getHighest(self):
        try:
            numOfHighestFreqInput = 5  # int(input("Number of highest frequencies letters: "))
        except:
            print("not a number....")
            exit(0)
        for i in range(numOfHighestFreqInput):
            print(f"letter {self.sortedFreqList[i][0]}:: {self.sortedFreqList[i][1]}")


    def PMF(self):
        plt.plot(self.x_letters, self.y_PMF)
        plt.show()
        pass

    def CDF(self):
        plt.plot(self.x_letters, self.y_CDF)
        plt.show()
        pass

    def mean(self):
        mean = np.sum(self.x_numbers * self.y_PMF)
        print(mean)

        variance = np.sum(self.x_numbers ** 2 * self.y_PMF) - mean ** 2
        # variance2 = sum((self.x_numbers-mean)**2 * PMF)
        print(np.sum(self.x_numbers * self.y_freq) / self.textFileLength)
        pass

    def variance(self):
        pass



App = Stat("text.txt")
App.calc()
# App.freqPlot()
# App.getHighest()
App.PMF()
App.CDF()