import string
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Button, Label, Entry


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

        self.mean = None
        self.variance = None

        # preparing letters lists
        # aAbBcC...012...789
        self.allLetersList = ""
        for i in range(len(string.ascii_lowercase)):
            self.allLetersList += string.ascii_lowercase[i] + string.ascii_uppercase[i]
        self.allLetersList += string.digits
        # preparing letters lists
        self.letterFreqDict = {}
        for letter in self.allLetersList:
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

        #calc mean
        self.mean = np.sum(self.x_numbers * self.y_PMF)
        #calc var
        self.variance = np.sum(self.x_numbers ** 2 * self.y_PMF) - self.mean ** 2
        # variance2 = sum((self.x_numbers-self.mean)**2 * PMF)

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

    def showMean(self):
        print(self.mean)
        print(self.variance)






# App = Stat("text.txt")
# App.calc()
# # App.freqPlot()
# # App.getHighest()
# # App.PMF()
# # App.CDF()
# App.showMean()


class GUIApp:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.config(bg="#1b1464", padx=50,pady=50)

        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)

        self.welcome = Label(self.frame, text="Welcome in T-Stat App\n", font='Arial 20 bold', bg='#1b1464', fg='#00ffc5')
        self.welcome.pack()

        self.fileNameEntry = Entry(self.frame,bg='#1b1464', fg='#ec008c')
        self.HighestNumEntry = Entry(self.frame,bg='#1b1464', fg='#ec008c')
        self.fileNameEntry.pack()
        self.HighestNumEntry.pack()




        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        # self.app = Demo2(self.newWindow)




def main():
    root = tk.Tk()
    root.title('T-Stat')
    root.minsize(500, 400)
    root.config(bg="#1b1464")
    # root.iconbitmap('icon.ico')

    App = GUIApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
