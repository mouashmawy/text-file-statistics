import string
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Button, Label, Entry
import sys
import math

#GLOBAL VARS
BK_CLR = "#1D7874"
FG_CLR = "#F4C095"
WRT_CLR = "#071E22"




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
        try:
            file = open("samples/"+textFileName, encoding='utf-8')
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
        # self.skewness = (self.mean - self.mode)/self.stdDeviation
        self.skewness = sum((self.x_numbers-self.mean)**3 * self.y_PMF)/self.stdDeviation**3
        #calc kurtosis
        fourthMoment = sum((self.x_numbers-self.mean)**4 * self.y_PMF)
        self.kurtosis = fourthMoment/self.variance**2


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
        plt.stem(self.x_letters, self.y_PMF)
        plt.show()
        pass

    def CDF(self):
        plt.plot(self.x_letters, self.y_CDF)
        plt.show()
        pass

    def getStatistics(self):
        text = f"Mean:{round(self.mean,2)}\nVariance:{round(self.variance,2)}\nSkewness:{round(self.skewness,2)}\nKurtosis:{round(self.kurtosis,2)}"
        return [["Mean",round(self.mean,2)],
                ["Variance",round(self.variance,2)],
                ["std dev",round(self.stdDeviation,2)],
                ["Skewness",round(self.skewness,2)],
                ["Kurtosis",round(self.kurtosis,2)]]



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
        #

        self.fileNameEntry = Entry(self.frame2, bg=BK_CLR, fg=WRT_CLR, font='Arial 14')
        # self.HighestNumEntry = Entry(self.frame2, bg=BK_CLR, fg=WRT_CLR)
        self.HighestNumEntry = tk.Scale(self.frame2, from_=0, to=30, orient="horizontal", bd=0,activebackground=BK_CLR, bg=WRT_CLR, fg=FG_CLR,troughcolor=BK_CLR, length=250,relief=tk.RAISED)

        self.fileNameLabel.grid(row=0,column=0)
        self.fileNameEntry.grid(row=1,column=0)
        self.HighestNumLabel.grid(row=2, column=0)
        self.HighestNumEntry.grid(row=3,column=0)

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
        self.someStatsButton = Button(self.frame4, text='some stats', command=self.showStats, bg=FG_CLR, padx=15, pady=10, borderwidth=4)
        self.exitButton = Button(self.frame4, text='Exit App', command=self.exiting, bg=FG_CLR, padx=15, pady=10, borderwidth=4)

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
        self.fileNameText = "sample.txt"#self.fileNameEntry.get()
        self.highestNumText =10 #self.HighestNumEntry.get()
        self.statsApp = Stat(self.fileNameText, int(self.highestNumText))
        self.statsApp.calc()
        self.processingLabel.config(text=f"processing {self.fileNameText} file with {self.highestNumText} most frequent...")


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

    def showStats(self):
        self.validate()
        self.additionalWindow1 = tk.Toplevel(self.master,bg=BK_CLR)
        self.additionalWindow1.minsize(400, 250)
        self.statsLabel = Label(self.additionalWindow1, text="Some Statistics", font='Arial 18 bold', bg=BK_CLR, fg=FG_CLR,pady=20)
        self.frameNew = tk.Frame(self.additionalWindow1,bg=BK_CLR)
        list = self.statsApp.getStatistics()
        tableFrame = self.createTable(self.frameNew, list)
        self.statsLabel.pack()
        tableFrame.pack()
        self.frameNew.pack()


    def validate(self):
        self.calculating()
        if self.additionalWindow1 != None:
            self.additionalWindow1.destroy()
        plt.close('all')
        pass

    def createTable(self, TableFrame, list):
        table = tk.Frame(TableFrame, bg=BK_CLR, padx=10, pady=10)
        for i in range(len(list)):
            for j in range(len(list[0])):
                e = Entry(table, width=10, bg=BK_CLR,fg=FG_CLR, font=('Arial', 16, 'bold')
                          ,disabledbackground=BK_CLR,disabledforeground=FG_CLR)
                e.grid(row=i, column=j)
                e.insert(tk.END, list[i][j])
                e.config(state=tk.DISABLED)
        return table


def main():
    root = tk.Tk()
    root.title('T-Stat App - Text File Statistics ')
    root.minsize(500, 400)
    root.config(bg=BK_CLR)
    # root.iconbitmap('icon.ico')

    App = GUIApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
