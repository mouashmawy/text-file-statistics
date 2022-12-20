import string
import matplotlib.pyplot as plt
import numpy as np
import math

class Stat:
    def __init__(self, filename:str,numOfHighestFreqInput:int):
        self.filename = filename
        self.numOfHighestFreqInput = numOfHighestFreqInput
        self.textFileLength=0
        self.textInFile = ""
        self.sortedFreqList =[]

        self.x_letters = None
        self.y_freq = None
        self.y_PMF = None
        self.y_CDF = None

        self.mean = None
        self.mode = None
        self.median = None
        self.variance = None
        self.stdDeviation = None
        self.skewness = None

        # preparing letters lists
        # aAbBcC...012...789
        self.allLetersList = ""
        self.allLetersList += string.digits
        for i in range(len(string.ascii_lowercase)):
            self.allLetersList += string.ascii_lowercase[i] + string.ascii_uppercase[i]

        # preparing the letters freq dictionary
        self.letterFreqDict = {}
        for letter in self.allLetersList:
            self.letterFreqDict[letter] = 0

        # Reading text from file
        textFileName = self.filename
        file=""
        try:
            file = open(f"{textFileName}", encoding='utf-8')
            tempTextInFile = file.read().replace(" ", "")
        finally:
            file.close()

        for letter in tempTextInFile:
            if letter in self.allLetersList:
                self.textInFile+=letter
        self.textFileLength = len(self.textInFile)

    def __str__(self):
        return f"File name: {self.filename}"


    def calc(self):
        for letter in self.textInFile:
            self.letterFreqDict[letter] += 1
        self.sortedFreqList = sorted(self.letterFreqDict.items(), key=lambda kv: kv[1], reverse=1)
        self.x_letters = np.array(list(self.letterFreqDict.keys()))
        self.y_freq = np.array(list(self.letterFreqDict.values()))

        # Generating PMF
        self.x_numbers = np.array(list(range( len(self.x_letters))))  # Generating a list starting 10 for a rnage in length letter list
        self.y_PMF = self.y_freq / self.textFileLength
        # Generating CDF
        self.y_CDF = self.y_PMF.copy()
        for i in range(1, len(self.y_PMF)):
            self.y_CDF[i] = self.y_CDF[i] + self.y_CDF[i - 1]

        #calc mean
        self.mean = np.sum(self.x_numbers * self.y_PMF)
        #calc var
        self.variance = np.sum(self.x_numbers ** 2 * self.y_PMF) - self.mean ** 2
        # self.variance = sum((self.x_numbers-self.mean)**2 * self.y_PMF) #another way to calc it

        #calc std deviation
        self.stdDeviation = math.sqrt(self.variance)

        #calc skewness

        modeLetter = self.sortedFreqList[0][0]
        self.mode= list(self.letterFreqDict.keys()).index(modeLetter)

        medianLetterIndex=len(self.sortedFreqList)/2

        if(isinstance(medianLetterIndex, int)):
            medianLetter = self.sortedFreqList[medianLetterIndex][0]
            self.median = list(self.letterFreqDict.keys()).index(medianLetter)
        else:
            medianLetter1 = self.sortedFreqList[int(medianLetterIndex)][0]
            medianLetter2 = self.sortedFreqList[int(medianLetterIndex)+1][0]
            self.median = (list(self.letterFreqDict.keys()).index(medianLetter1) + list(self.letterFreqDict.keys()).index(medianLetter2))/2

            # self.skewness = (self.mean - self.mode)/self.stdDeviation
        self.skewness = sum((self.x_numbers-self.mean)**3 * self.y_PMF)/self.stdDeviation**3
        #calc kurtosis
        fourthMoment = sum((self.x_numbers-self.mean)**4 * self.y_PMF)
        self.kurtosis = fourthMoment/self.variance**2


    def freqPlot(self):
        f = plt.figure()
        f.set_figwidth(13)
        plt.stem(self.x_letters, self.y_freq)
        plt.show()
        pass


    def getHighestList(self):
        num = self.numOfHighestFreqInput
        return self.sortedFreqList[:num]


    def PMF(self):
        f = plt.figure()
        f.set_figwidth(13)
        plt.stem(self.x_letters, self.y_PMF)
        plt.show()
        pass

    def CDF(self):
        f = plt.figure()
        f.set_figwidth(13)
        plt.plot(self.x_letters, self.y_CDF)
        plt.show()
        pass

    def getStatistics(self):
        return [["Char count", round(self.textFileLength, 0)],
                ["Mean",round(self.mean,2)],
                ["Mode", round(self.mode, 2)],
                ["Median", round(self.median, 2)],
                ["Variance",round(self.variance,2)],
                ["std dev",round(self.stdDeviation,2)],
                ["Skewness",round(self.skewness,2)],
                ["Kurtosis",round(self.kurtosis,2)]]

