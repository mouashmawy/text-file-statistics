import string
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Button, Label, Entry
import sys

#GLOBAL VARS
BK_CLR = "#1b1464"
FG_CLR = "#00ffc5"




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
        # plt.bar(self.x_letters, self.y_freq)
        # plt.show()
        plt.plot(self.x_letters, self.y_freq)
        plt.show()
        pass


    def getHighest(self):
        TextOfHighest =""
        for i in range(self.numOfHighestFreqInput):
            TextOfHighest+=f"letter {self.sortedFreqList[i][0]}:: {self.sortedFreqList[i][1]}\n"
        return TextOfHighest


    def PMF(self):
        plt.plot(self.x_letters, self.y_PMF)
        plt.show()
        pass

    def CDF(self):
        plt.plot(self.x_letters, self.y_CDF)
        plt.show()
        pass

    def getMean(self):
        text = f"Mean:{self.mean}\nVariance:{self.variance}"
        return text



class GUIApp:
    def __init__(self, master):
        self.master = master
        self.additionalWindow1 = None
        self.fileNameText = None
        self.highestNumText = None
        self.statsApp = None
        ##########frame 1
        self.frame1 = tk.Frame(self.master,bg=BK_CLR, padx=50,pady=50)
        self.welcome = Label(self.frame1, text="Welcome in T-Stat App", font='Arial 20 bold', bg=BK_CLR, fg=FG_CLR)
        self.welcome.grid(row=0,column=0)

        ##########frame 2
        self.frame2 = tk.Frame(self.master,bg=BK_CLR, padx=10,pady=10)
        self.fileNameLabel = Label(self.frame2, text="File Name", font='Arial 11', bg=BK_CLR, fg=FG_CLR)
        self.HighestNumLabel = Label(self.frame2, text="# of Highest", font='Arial 11', bg=BK_CLR, fg=FG_CLR)
        self.fileNameLabel.grid(row=0,column=0)
        self.HighestNumLabel.grid(row=0,column=1)

        self.fileNameEntry = Entry(self.frame2, bg=BK_CLR, fg='#ec008c')
        self.HighestNumEntry = Entry(self.frame2, bg=BK_CLR, fg='#ec008c')
        self.fileNameEntry.grid(row=1,column=0)
        self.HighestNumEntry.grid(row=1,column=1)

        ##########frame 3
        self.frame3 = tk.Frame(self.master,bg=BK_CLR,padx=10,pady=10)
        self.enterButton = Button(self.frame3, text='ENTER', command=self.calculating,bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.processingLabel = Label(self.frame3, text=f"Enter file name and number...", font='Arial 11', bg=BK_CLR, fg=FG_CLR)

        self.enterButton.grid(row=0,column=0)
        self.processingLabel.grid(row=1,column=0)

        ##########frame 4
        self.frame4 = tk.Frame(self.master, bg=BK_CLR, padx=10, pady=10)
        self.freqButton = Button(self.frame4, text='Freq graph', command=self.showFreqGraph, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.numHighestButton = Button(self.frame4, text='Most Freq', command=self.showHighestFreq, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.PMFButton = Button(self.frame4, text='show PMF', command=self.showPMF, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.CDFButton = Button(self.frame4, text='show CDF', command=self.showCDF, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.someStatsButton = Button(self.frame4, text='some stats', command=self.showMean, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.exitButton = Button(self.frame4, text='Exit', command=self.exiting, bg=FG_CLR, padx=15, pady=10, borderwidth=4)

        self.freqButton.grid(row=0,column=0)
        self.numHighestButton.grid(row=0,column=1)
        self.PMFButton.grid(row=1,column=0)
        self.CDFButton.grid(row=1,column=1)
        self.someStatsButton.grid(row=2, column=0)
        self.exitButton.grid(row=2, column=1)



        #frames
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

    def exiting(self):
        sys.exit("Thanks for using T-Stat App...")

    def calculating(self):
        self.fileNameText = self.fileNameEntry.get()
        self.highestNumText = self.HighestNumEntry.get()
        self.statsApp = Stat(self.fileNameText, int(self.highestNumText))
        self.statsApp.calc()
        self.processingLabel.config(text=f"processing {self.fileNameText} file with {self.highestNumText} most frequent")


    def showFreqGraph(self):
        self.validate()
        self.statsApp.freqPlot()


    def showHighestFreq(self):
        self.validate()
        if self.additionalWindow1 != None:
            self.additionalWindow1.destroy()

        self.additionalWindow1 = tk.Toplevel(self.master)

        self.frameNew = tk.Frame(self.additionalWindow1)
        textOfHighest = self.statsApp.getHighest()
        Label(self.frameNew, text=textOfHighest, font='Arial 16', bg=BK_CLR, fg=FG_CLR).pack()
        self.frameNew.pack()


    def showPMF(self):
        self.validate()
        self.statsApp.PMF()


    def showCDF(self):
        self.validate()
        self.statsApp.CDF()

    def showMean(self):
        self.validate()
        self.additionalWindow1 = tk.Toplevel(self.master)

        self.frameNew = tk.Frame(self.additionalWindow1)
        textToShow = self.statsApp.getMean()
        Label(self.frameNew, text=textToShow, font='Arial 16', bg=BK_CLR, fg=FG_CLR).pack()
        self.frameNew.pack()


    def validate(self):
        self.calculating()
        if self.additionalWindow1 != None:
            self.additionalWindow1.destroy()
        plt.close('all')
        pass

def main():
    root = tk.Tk()
    root.title('T-Stat App - Text File Statistics ')
    root.minsize(500, 400)
    root.config(bg=BK_CLR)
    root.iconbitmap('icon.ico')

    App = GUIApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
