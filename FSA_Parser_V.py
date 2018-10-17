#A Python script designed to parse loan details from an FSA download
#Currently only supports .txt files
#Brian Sloan
#10/15/2018
#v1.0

from tkinter import *

class Loan:
    id=""
    bal=0
    status=""
    servicer=""
    parent=False
    
    def toString(self):
        if self.parent == True:
            return "ID#:  {0}\nBalance:  ${1}\nStatus:  {2}\nServicer:  {3}\nParent Plus".format(self.id, self.bal, self.status, self.servicer)
        else:
            return "ID#:  {0}\nBalance:  ${1}\nStatus:  {2}\nServicer:  {3}".format(self.id, self.bal, self.status, self.servicer)

loans = []

#Pulls commas out of numbers
def handleNum(num_str):
    if num_str == "":
        return 0
    if len(num_str)<4:
        return int(num_str)
    else:
        return int(num_str[:-4]+num_str[-3:])

#Returns the verification-relevant status of a loan.  WILL NOT RETURN FORBEARANCE IF IN FORBEARANCE.
def status(stat):
    if stat == "RP":
        return "Current"
    elif stat == "FB":
        return "Current"
    elif stat == "DA":
        return "Current"
    elif stat == "IG":
        return "Current"
    elif stat == "IP":
        return "Current"
    elif stat == "IA":
        return "Loan Originated"
    elif stat == "DF":
        return "Defaulted"
    elif stat == "DU":
        return "Defaulted"
    elif stat == "DX":
        return "Defaulted"
    elif stat == "DP":
        return "Paid In Full"
    elif stat == "PF":
        return "Paid In Full"
    elif stat == "CA":
        return "Canceled"
    elif stat == "DN":
        return "Consolidated"
    elif stat == "PN":
        return "Consolidated"
    elif stat == "PC":
        return "Consolidated"
    else:
        return "UNKNOWN"

#Prints the "at a glance" details verification needs:  Balance, status, servicers, and a short breakdown by status and servicer
def printSummary():
    sum = 0
    servicers = []
    stat = []
    pp = False
    tstring=""

    for loan in loans:
        sum+=loan.bal
        if loan.servicer not in servicers:
            servicers.append(loan.servicer)
        if loan.status not in stat:
            if loan.status != "Canceled":
                if loan.status != "Consolidated":
                    if loan.status != "Paid In Full":
                        stat.append(loan.status)
        if loan.parent == True:
            pp = True
            
    tstring="Total Balance:  ${0}\nStatus:  {1}".format(sum, stat)
    
    if len(stat)>1:
        for s in stat:
            sum = 0
            for loan in loans:
                if loan.status == s:
                    sum+= loan.bal
            tstring+="\nTotal {0}:  ${1}".format(s, sum)
    
    for s in servicers:
        sum = 0
        for loan in loans:
            if loan.servicer == s:
                sum += loan.bal
        tstring+="\n{0}:  ${1}".format(s, sum)
        
    if pp == True:
        sum = 0
        sumParent = 0
        for loan in loans:
            if loan.parent == True:
                sumParent+= loan.bal
            else:
                sum+= loan.bal
        tstring+="\nParent Plus Total:  ${0}\nNon-Parent Plus Total:  ${1}".format(sumParent, sum)
    summary_T.insert(END, tstring)

#Reads in each loan
def textParse(filename):
    i=-1
    f = open(filename)
    for line in f:
        if line[:9] == "Loan Type":
            i+=1
            loans.append(Loan())
            if "PARENT" in line:
                loans[i].parent=True
           
        elif line[:13] == "Loan Award ID":
            loans[i].id=line[14:-1]
        
        elif line[:34] == "Loan Outstanding Principal Balance":
            if "as" not in line:
                loans[i].bal=int(handleNum(line[36:-1]))

        elif line[:33] == "Loan Outstanding Interest Balance":
            if "as" not in line:
                loans[i].bal+=int(handleNum(line[35:-1]))
        
        elif line[:11] == "Loan Status":
            if loans[i].status == "":
                loans[i].status=status(line[12:-1])
                
                #double-default check
                if loans[i].status == "Defaulted":
                    line = f.readline()
                    ddFlag = False
                    while line[:11] == "Loan Status":
                        if line[12:-1] == "RP":
                            ddFlag = True
                        if status(line[12:-1]) == "Defaulted":
                            if ddFlag == True:
                                loans[i].status = "Double Defaulted"
                                ddFlag = False
                        line = f.readline()
                    ddFlag = False
           
        if line[:17] == "Loan Contact Name":
            loans[i].servicer = line[18:-1]

    printSummary()
    detailsText = ""
    for loan in loans:
        detailsText+=loan.toString()
        detailsText+="\n\n"
    details_T.insert(END, detailsText)
                
#Currently unsupported due to file inconsistency
def csvParse(filename):
    i=-1
    f = open(filename)
    for line in f:
        if line[1:10] == "Loan Type":
            i+=1
            loans.append(Loan())
            if "PARENT" in line:
                loans[i].parent=True
           
        elif line[1:14] == "Loan Award ID":
            loans[i].id=line[17:-2]
        
        elif line[1:35] == "Loan Outstanding Principal Balance":
            if "as" not in line:
                loans[i].bal=int(handleNum(line[39:-2]))

        elif line[1:34] == "Loan Outstanding Interest Balance":
            if "as" not in line:
                loans[i].bal+=int(handleNum(line[38:-2]))
        
        elif line[1:12] == "Loan Status":
            if loans[i].status == "":
                loans[i].status=status(line[15:-2])
                if loans[i].status == "Defaulted":
                    line = f.readline()
                    ddFlag = False
                    while line[1:12] == "Loan Status":
                        if line[15:-2] == "RP":
                            ddFlag = True
                        if status(line[15:-2]) == "Defaulted":
                            if ddFlag == True:
                                loans[i].status = "Double Defaulted"
                                ddFlag = False
                        line = f.readline()
                    ddFlag = False
           
        if line[1:18] == "Loan Contact Name":
            loans[i].servicer = line[21:-2]
                
    printSummary()
    detailsText = ""
    for loan in loans:
        detailsText+=loan.toString()
        detailsText+="\n\n"
    details_T.insert(END, detailsText)

#Button function; parses the file if it is valid, otherwise do nothing.
def onRun():
    filename = file_E.get()
    try:
        open(filename)
    except OSError:
        a=0
    while len(loans)>0:
        loans.pop(0)
    summary_T.delete('1.0', END)
    details_T.delete('1.0', END)
    if filename[-3:] == "txt":
        textParse(filename)
    elif filename[-3:] == "csv":
        csvParse(filename)

#Sets up the GUI
root = Tk()
root.geometry("800x500+500+150")
root.resizable(False, False)

summary_F = Frame(root)
summary_F.place(x=200, width = 800-250, height=150)

summary_S = Scrollbar(summary_F)
summary_T = Text(summary_F)
summary_S.pack(side=RIGHT, fill = Y)
summary_T.pack(fill = Y)
summary_S.config(command=summary_T.yview)
summary_T.config(yscrollcommand=summary_S.set)

details_F = Frame(root)
details_F.place(x=200, y=150, width = 800-250, height = 350)

details_S = Scrollbar(details_F)
details_T = Text(details_F)
details_S.pack(side=RIGHT, fill = Y)
details_T.pack(fill = Y)
details_S.config(command=details_T.yview)
details_T.config(yscrollcommand=details_S.set)

title_L = Label(root, text = "FSA Parser", font = "times 24")
title_L.place(x=10, y=10)

run_B = Button(root, text = "run", command = onRun)
run_B.place(x=150, y=80)

file_L = Label(root, text = "Enter File (include extension!)")
file_L.place(x=10, y=60)
file_E = Entry(root)
file_E.place(x=10, y=80, height = 25)

root.mainloop()