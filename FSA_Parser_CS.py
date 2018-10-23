from datetime import date
from datetime import timedelta
from tkinter import *
import FSA_Library as fsa

def printSummary(student):
    sum = 0
    sumPay = 0
    servicers = []
    stat = []
    pp = False
    tstring=""

    for loan in student.loans:
        sum+=loan.bal
        sumPay+=loan.paymentAmount
        if loan.servicer not in servicers:
            servicers.append(loan.servicer)
        if loan.status not in stat:
            if loan.status != "Canceled":
                if loan.status != "Consolidated":
                    if loan.status != "Paid In Full":
                        stat.append(loan.status)
        if loan.parent == True:
            pp = True
            
    tstring="Total Balance:  ${0}\nStatus:  {1}\nTotal Payment:  ${2}\nPayment Date:  {3}".format(sum, ", ".join(stat), sumPay, student.loans[0].paymentDate)
    
    if len(stat)>1:
        for s in stat:
            sum = 0
            for loan in student.loans:
                if loan.status == s:
                    sum+= loan.bal
            if sum> 0:
                tstring+="\nTotal {0}:  ${1}".format(s, sum)
    
    for s in servicers:
        sum = 0
        for loan in student.loans:
            if loan.servicer == s:
                sum += loan.bal
        tstring+="\n{0}:  ${1}".format(s, sum)
        
    if pp == True:
        sum = 0
        sumParent = 0
        for loan in student.loans:
            if loan.parent == True:
                sumParent+= loan.bal
            else:
                sum+= loan.bal
        tstring+="\nParent Plus Total:  ${0}\nNon-Parent Plus Total:  ${1}".format(sumParent, sum)
    summary_T.insert(END, tstring)


#Button function; parses the file if it is valid, otherwise do nothing.
def onRun():
    summary_T.delete('1.0', END)
    details_T.delete('1.0', END)

    try:
        student = fsa.Student()
        while student.loans != []:                 #for some abominable reason, python is allergic to clearing memory
            student.loans.pop()                    #this awful workaround is necessary to avoid "ghost" loans
        
        student = fsa.textParse(file_E.get())

        printSummary(student)
        detailsText = ""
        for loan in student.loans:
            detailsText+=loan.csToString()
            detailsText+="\n\n"
        details_T.insert(END, detailsText)

    except OSError:
        pass

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