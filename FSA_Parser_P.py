from datetime import date
from datetime import timedelta
from tkinter import *
import FSA_Library as fsa

       
def printSummary(student):
    loanStat = []
    servicers = []
    bal = 0
    f = open(student.name+".txt", "w+")
    
    for ghost in loanStat:
        loanStat.pop()
    for ghost in servicers:
        servicers.pop()
        
    f.write(student.toString())
    summary_T.insert(END, student.toString())
    
    for loan in student.loans:
        if loan.status not in loanStat:
            
            if loan.status == "Repayment":
                loanStat.append(loan.status)
            if loan.status == "Loan Originated":
                loanStat.append(loan.status)
            if loan.status == "Defaulted":
                loanStat.append(loan.status)
            if loan.status == "Double Defaulted":
                loanStat.append(loan.status)
                
    if loanStat == []:
        loanStat.append(student.loans[0].status)
                
    f.write("\nLoan Status:  {0}".format(", ".join(loanStat)))
    summary_T.insert(END, "\nLoan Status:  {0}".format(", ".join(loanStat)))
    
    if len(loanStat) > 1:
        for stat in loanStat:
            statBal = 0
            for loan in student.loans:
                if loan.status == stat:
                    statBal += loan.bal
            f.write("\n{0}:  ${1}".format(stat, statBal))
            summary_T.insert(END, "\n{0}:  ${1}".format(stat, statBal))
            
    for loan in student.loans:
        if loan.servicer not in servicers:
            servicers.append(loan.servicer)
            
    if len(servicers) == 1:
        f.write("\nLoan Servicer:  {0}".format(servicers[0]))
        summary_T.insert(END, "\nLoan Servicer:  {0}".format(servicers[0]))
    else:
        for servicer in servicers:
            servBal = 0
            for loan in student.loans:
                if loan.servicer == servicer:
                    servBal += loan.bal
            if servBal != 0:
                f.write("\n{0}:  ${1}".format(servicer, servBal))
                summary_T.insert(END, "\n{0}:  ${1}".format(servicer, servBal))
    
    for loan in student.loans:
        bal += loan.bal
    if student.bal() != bal:
        f.write("\n\n\nSummary incomplete.  Please run again with most recent version.")
        summary_T.insert(END, "\nHey, send this file to Brian!  New loan type identifier.")

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
            detailsText+=loan.pToString()
            detailsText+="\n\n"
        f = open(student.name+".txt", "a+")
        f.write("\n\n\n\n" + detailsText)
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