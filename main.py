import string
import matplotlib.pyplot as plt
import numpy as np

#preparing letters lists
#aAbBcC...012...789
allLetersList=""
for i in range(len(string.ascii_lowercase)):
    allLetersList+=string.ascii_lowercase[i]+string.ascii_uppercase[i]
allLetersList+=string.digits

#preparing letters lists
letterFreqDict = {}
for letter in allLetersList:
    letterFreqDict[letter] = 0


#Reading text from file
textFileName ="text.txt"
textInFile = ""
try:
    file = open(textFileName, encoding = 'utf-8')
    textInFile = file.read().replace(" ","")
    textFileLength = len(textInFile)
finally:
    file.close()


for letter in textInFile:
    letterFreqDict[letter] +=1



sortedFreqList = sorted(letterFreqDict.items(), key=lambda kv:kv[1],reverse=1)

try:
    numOfHighestFreqInput = 5#int(input("Number of highest frequencies letters: "))
except:
    print("not a number....")
    exit(0)


for i in range(numOfHighestFreqInput):
    print(f"letter {sortedFreqList[i][0]}:: {sortedFreqList[i][1]}")


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