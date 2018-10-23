from datetime import date
from datetime import timedelta

class Student:
    name = ""
    status = ""
    ffel = 0
    dir = 0
    ffelConsolidated = 0
    perkins = 0
    dirConsolidated = 0
    grad = 0
    parent = 0
    sls = 0
    loans = []
    
    def bal(self):
        return self.ffel + self.dir + self.ffelConsolidated + self.dirConsolidated + self.perkins + self.parent + self.grad + self.sls
    
    def toString(self):
        str = "Name:  {0}\nSchool Status:  {1}\nTotal Balance:  ${2}".format(self.name, self.status, self.bal())

        if self.ffel != 0:
            str+="\nTotal FFEL Stafford:  ${0}".format(self.ffel)
                
        if self.dir != 0:
            str+="\nTotal Direct Stafford:  ${0}".format(self.dir)
        
        if self.ffelConsolidated != 0:
            str+="\nTotal FFEL Consolidated:  ${0}".format(self.ffelConsolidated)
        
        if self.perkins != 0:
            str+="\nTotal Federal Perkins:  ${0}".format(self.perkins)
        
        if self.dirConsolidated != 0:
            str+="\nTotal Direct Consolidated:  ${0}".format(self.dirConsolidated)
        
        if self.grad != 0:
            str+="\nTotal Graduate Plus:  ${0}".format(self.grad)
        
        if self.parent != 0:
            str+="\nTotal Parent Plus:  ${0}".format(self.parent)
        
        if self.sls != 0:
            str+="\nTotal FFEL Supplemental:  ${0}".format(self.sls)
        
        return str
        
class Loan:
    id=""
    bal=0
    status=""
    paymentDate=""
    paymentAmount=0
    servicer=""
    parent=False
    perkins=False
    forbTime=timedelta()
    type=""
    idrType=""
    idrStart=""
    idrAniv=""
    servicerAddr=""
    
    def pToString(self):
        str = "Type:  {0}\nBalance:  ${1}\nStatus:  {2}\nRepayment Plan:  {3}\nPayment Amount:  ${4}\nPayment Date:  {5}".format(self.type, self.bal, self.status, self.idrType, self.paymentAmount, self.paymentDate)

        if self.idrType != "STANDARD REPAYMENT":
            if self.idrType != "":
                str += "\nRepayment Plan Start Date:  {0}\nRepayment Plan Aniversary:  {1}".format(self.idrStart, self.idrAniv)

        str += "\nServicer:  {0}".format(self.servicer)
        
        if self.status == "Defaulted" or self.status == "Double Defaulted":
            str += "\n{0}".format(self.servicerAddr)
            
        str += "\nForbearance Time Remaining:  {0}".format(1095-self.forbTime.days)
        return str
        
    def csToString(self):
        str = "ID#:  {0}\nBalance:  ${1}\nStatus:  {2}".format(self.id, self.bal, self.status)

        if self.status != "Forbearance":
            str += "\nNext Payment Date:  {0}\nNext Payment Amount:  ${1}".format(self.paymentDate, self.paymentAmount)
            
        str += "\nServicer:  {0}".format(self.servicer)
        
        if self.parent == True:
            str +="\nParenet Plus Loan"
        
        str +="\nForbearance Time Remaining:  {0} Days".format(1095-self.forbTime.days)
        return str
    
    def verToString(self):
        if self.parent == True:
            return "ID#:  {0}\nBalance:  ${1}\nStatus:  {2}\nServicer:  {3}\nParent Plus".format(self.id, self.bal, self.status, self.servicer)
        else:
            return "ID#:  {0}\nBalance:  ${1}\nStatus:  {2}\nServicer:  {3}".format(self.id, self.bal, self.status, self.servicer)

def fixReadLine(f):
    str = f.readline()
    while str == "\n":
        str = f.readline()
    return str

#Pulls commas out of numbers and slashes out of dates
def handleNum(str):
    if str == "":
        return 0
    if "/" in str:
        dateStr = []
        tempStr = ""
        i=0
        
        for char in str:
            if char.isnumeric():
                tempStr+=char
            elif char == '/':
                dateStr.append(tempStr)
                tempStr = ""
                i+=1
        dateStr.append(tempStr)
        return date(int(dateStr[2]), int(dateStr[0]), int(dateStr[1]))

    else:
        num = ""
        for char in str:
            if char.isnumeric():
                num+=char
        if num == "":
            return 0
        return int(num)
    
#Format-independent way of pulling useful data out of a line
def dirtyParse(str):
    #print("x")
    #print(str)
    try:
        i=0
        data = []
        while (str[i] != ":" and str[i] != ","):
            i+=1
        i+=1
        while str[i] != "\n":
            if str[i] != "\"":
                data.append(str[i])
            i+=1
        return "".join(data)
    except IndexError:
        print("DIRTY PARSE")
        print(str)
        print(data)
        print(i)
        return ""

#Turns the two-character code into the effective status
def status(stat):
    if stat == "RP":
        return "Repayment"
    elif stat == "FB":
        return "Forbearance"
    elif stat == "DA":
        return "Deferment"
    elif stat == "IG":
        return "Grace Period"
    elif stat == "IP":
        return "Deferment"
    elif stat == "IA":
        return "Loan Originated"
    elif stat == "DF":
        return "Defaulted"
    elif stat == "DX":
        return "Defaulted"
    elif stat == "DU":
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
    
def textParse(filename):
    student = Student()
    f = open(filename)
    i=-1
    line = fixReadLine(f)
    
    while line != "":
        
        if "Student First Name" in line:
            student.name = dirtyParse(line)
            fixReadLine(f)
            line = fixReadLine(f)
            student.name += " " + dirtyParse(line)
            
        if "Student Enrollment Status" in line:
            student.status = dirtyParse(line)
            fixReadLine(f)
            
        if "Total FFEL STAFFORD SUBSIDIZED" in line:
            student.ffel += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.ffel += handleNum(dirtyParse(line))
            
        if "Total FFEL STAFFORD UNSUBSIDIZED" in line:
            student.ffel += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.ffel += handleNum(dirtyParse(line))
            
        if "Total DIRECT STAFFORD UNSUBSIDIZED" in line:
            student.dir += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.dir += handleNum(dirtyParse(line))
            
        if "Total DIRECT STAFFORD SUBSIDIZED" in line:
            student.dir += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.dir += handleNum(dirtyParse(line))
            
        if "Total FFEL CONSOLIDATED" in line:
            student.ffelConsolidated += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.ffelConsolidated += handleNum(dirtyParse(line))
            
        if "Total FEDERAL PERKINS" in line:
            student.perkins += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.perkins += handleNum(dirtyParse(line))
            
        if "Total DIRECT CONSOLIDATED UNSUBSIDIZED" in line:
            student.dirConsolidated += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.dirConsolidated += handleNum(dirtyParse(line))
            
        if "Total DIRECT CONSOLIDATED SUBSIDIZED" in line:
            student.dirConsolidated += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.dirConsolidated += handleNum(dirtyParse(line))
            
        if "Total FFEL PLUS GRADUATE" in line:
            student.grad += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.grad += handleNum(dirtyParse(line))
            
        if "Total DIRECT PLUS GRADUATE" in line:
            student.grad += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.grad += handleNum(dirtyParse(line))
            
        if "Total FFEL STAFFORD NON-SUBSIDIZED" in line:
            student.ffel += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.ffel += handleNum(dirtyParse(line))
            
        if "Total DIRECT PARENT PLUS" in line:
            student.parent += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.parent += handleNum(dirtyParse(line))
            
        if "Total DIRECT PLUS PARENT" in line:
            student.parent += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.parent += handleNum(dirtyParse(line))
            
        if "Total FFEL PLUS PARENT" in line:
            student.parent += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.parent += handleNum(dirtyParse(line))
            
        if "Total FFEL SUPPLEMENTAL LOAN" in line:
            student.sls += handleNum(dirtyParse(line))
            line = fixReadLine(f)
            student.sls += handleNum(dirtyParse(line))        
            
        if "Loan Type" in line:
            i+=1
            student.loans.append(Loan())
            student.loans[i].type = dirtyParse(line)
            
            if "PERKINS" in line:
                student.loans[i].perkins = True
            if "PARENT" in line:
                student.loans[i].parent = True
        
        if "Loan Award ID" in line:
            student.loans[i].id = dirtyParse(line)
            
        if "Loan Outstanding Principal Balance" in line:
            #print(line)
            student.loans[i].bal = handleNum(dirtyParse(line))
            fixReadLine(f)
            line = fixReadLine(f)
            try:
                student.loans[i].bal += handleNum(dirtyParse(line))
                line = fixReadLine(f)
                line = fixReadLine(f)
            except TypeError:
                #print("LOAN BALANCE")
                #print(line)
                line = fixReadLine(f)
                line = fixReadLine(f)
            #print(line)

        if "Loan Next Payment Due Date" in line:
            student.loans[i].paymentDate = handleNum(dirtyParse(line))
        
        if "Loan Repayment Plan Type" in line:
            student.loans[i].idrType = dirtyParse(line)
            
        if "Loan Repayment Plan Begin Date" in line:
            student.loans[i].idrStart = dirtyParse(line)
        
        if "Loan Repayment Plan IDR Plan Anniversary Date" in line:
            student.loans[i].idrAniv = dirtyParse(line)
            
        if "Loan Repayment Plan Scheduled Amount" in line:
            student.loans[i].paymentAmount = handleNum(dirtyParse(line))
            
        if "Loan Status" in line:
            if student.loans[i].status == "":
                student.loans[i].status = status(dirtyParse(line))
                
                #Forb time and Double Defaulted checks
                ddFlag1 = ddFlag2 = False
                if student.loans[i].status == "Defaulted":
                    ddFlag1 = True
                    
                if student.loans[i].status == "Forbearance":
                    fixReadLine(f)
                    line = fixReadLine(f)
                    lastStatDate = handleNum(dirtyParse(line))
                    student.loans[i].forbTime += date.today() - lastStatDate
                    line = fixReadLine(f)
                else:
                    fixReadLine(f)
                    line = fixReadLine(f)
                    lastStatDate = handleNum(dirtyParse(line))
                    line = fixReadLine(f)
                    
                while "Loan Status" in line:

                    #Double Default
                    if "RP" in line:
                        ddFlag2 = True
                    if status(dirtyParse(line)) == "Defaulted":
                        if ddFlag1 & ddFlag2:
                            student.loans[i].status = "Double Defaulted"
                            ddFlag1 = ddFlag2 = False
                    
                    #Forb time
                    if "FB" in line:
                        fixReadLine(f)
                        line = fixReadLine(f)
                        student.loans[i].forbTime += lastStatDate - handleNum(dirtyParse(line))
                        lastStatDate = handleNum(dirtyParse(line))
                    else:
                        fixReadLine(f)
                        line = fixReadLine(f)
                        lastStatDate = handleNum(dirtyParse(line))
                        
                    line = fixReadLine(f)
                    
                ddFlag1 = ddFlag2 = False
                        
        if "Loan Contact Name" in line:
            student.loans[i].servicer = dirtyParse(line)
        
        if "Loan Contact Street Address 1" in line:
            student.loans[i].servicerAddr = dirtyParse(line)                 #addr 1
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "\n" + dirtyParse(line)     #addr2
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "\n" + dirtyParse(line)     #city
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += ", " + dirtyParse(line)     #state
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "  " + dirtyParse(line)     #zip
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "\n" + dirtyParse(line)     #phone
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += " ex. " + dirtyParse(line)  #ex
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "\n" + dirtyParse(line)     #email
            line = fixReadLine(f)
            if dirtyParse(line) != "":
                student.loans[i].servicerAddr += "\n" + dirtyParse(line)     #web
            
            
        line = fixReadLine(f)
    #print(len(student.loans))
    return student