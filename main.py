from tkinter import *
import hashlib

def MainWindowSetup():
    mainWindow.title('Health Tests')
    mainWindow.geometry('500x500')

    mainLabel.pack()
    profileBtn.pack()
    testsLabel.pack()
    for test in tests:
        for widget in test:
            widget.pack()
    if userData['login']=='admin':
        addTestBtn.pack()

def LoadTestsList():
    widgets=[]
    with open('tests.txt') as file:
        for line in file:
            widgets.append([Label(mainWindow,text=line.split(' ')[1].replace('_',' ')),Button(mainWindow,text='Start',command=lambda Id=line.split(' ')[0]: TestIntroWindowSetup(Id))])
    return widgets

def LoadTest(Id):
    activeTest['id']=Id
    with open('tests.txt') as file:
        for line in file:
            if Id==line.split(' ')[0]:
                activeTest['name']=line.split(' ')[1].replace('_',' ')
                activeTest['description']=line.split(' ')[2][:-1].replace('_',' ')
                break
    activeTest['questions']=[]
    activeTest['answers']=[]
    activeTest['answerValues']=[]
    with open('questions.txt') as file:
        for line in file:
            if line.split(' ')[0]==Id:
                args=line.split(' ')
                activeTest['questions'].append(args[1].replace('_',' '))
                activeTest['answers'].append(args[2].split(';'))
                activeTest['answerValues'].append(args[3].split(';'))
        for values in activeTest['answerValues']:
            values[-1]=values[-1][:-1]

def TestWindowInitSetup():
    testWindow.geometry('500x500')

def TestIntroWindowSetup(Id):
    LoadTest(Id)
    testWindow.title(activeTest['name'])
    testName['text']=activeTest['name']
    testDescription['text']=activeTest['description']

    testName.pack()
    testDescription.pack()
    startTestBtn.pack()
    
    testWindow.deiconify()
    mainWindow.withdraw()

def TestPassWindowSetup():
    global questionLabels
    global answerRadio
    global testResults
    testDescription.pack_forget()
    startTestBtn.pack_forget()
    backBtn.pack_forget()
    testResults=[]
    questionLabels=[]
    answerRadio=[]
    for i in range(len(activeTest['questions'])):
        testResults.append(StringVar(value='0'))
        questionLabels.append(Label(testWindow,text=activeTest['questions'][i]))
        questionLabels[i].pack()
        answerRadio.append([])
        for j in range(len(activeTest['answers'][i])):
            answerRadio[i].append(Radiobutton(testWindow,text=activeTest['answers'][i][j],
                                                         value=activeTest['answerValues'][i][j],
                                                         variable=testResults[i]))
            answerRadio[i][j].pack()
    startTestBtn.pack()
    startTestBtn['text']='Finish'
    startTestBtn['command']=GetResults

def ClearTestWindow():
    for i in range(len(questionLabels)):
        questionLabels[i].pack_forget()
        for j in range(len(answerRadio[i])):
            answerRadio[i][j].pack_forget()
    startTestBtn.pack_forget()
    testDescription.pack()
    startTestBtn.pack()
    startTestBtn['text']='Start test'
    startTestBtn['command']=TestPassWindowSetup
    backBtn.pack()

def GetResults():
    for i in range(len(testResults)):
        testResults[i]=int(testResults[i].get())
    res=sum(testResults)
    with open('results.txt') as file:
        for line in file:
            if line.split(' ')[0]==activeTest['id']:
                borders=line.split(' ')[1].split('-')
                if res>=int(borders[0]) and res<=int(borders[1]):
                    res=line.split(' ')[2].replace('_',' ')[:-1]
                    break
    ClearTestWindow()
    testWindow.withdraw()
    resultWindow.deiconify()
    resultText['text']=res

    lines=[]
    with open('passedTests.txt') as file:
        for line in file:
            lines.append(line)
    found=False
    for i in range(len(lines)):
        if lines[i].find(f"{userData['login']} {activeTest['id']}")>-1:
            found=True
            lines[i]=f"{userData['login']} {activeTest['id']} {res.replace(' ','_')}\n"
            break
    if not found:
        with open('passedTests.txt','a') as file:
            file.write(f"{userData['login']} {activeTest['id']} {res.replace(' ','_')}\n")
        return
    with open('passedTests.txt','w') as file:
        for line in lines:
            file.write(line)

def AuthWindowSetup():
    authWindow.title('Authentication')
    authWindow.geometry('200x200')

    authLabel.pack()
    loginLabel.pack()
    loginEntry.pack()
    passwordLabel.pack()
    passwordEntry.pack()
    btnLogin.pack()
    errorLabel.pack()
    btnRegister.pack()

def SignIn():
    login=loginEntry.get()
    userFound=False
    global userData
    with open('users.txt') as file:
        for line in file:
            attributes=line.split(' ')
            if attributes[0]==login:
                userFound=True
                userData={'login':attributes[0],'password':attributes[1][:-1]}
                break
    if not userFound:
        errorLabel['text']='Error: no user found with this login'
        return
    password=hashlib.sha3_256(passwordEntry.get().encode()).hexdigest()
    if not password==userData['password']:
        errorLabel['text']='Error: wrong password'
        return
    errorLabel['text']=' '
    authWindow.withdraw()
    MainWindowSetup()
    mainLabel['text']=f'Hello {userData["login"]}'
    mainWindow.deiconify()

def SignUp():
    login=loginEntry.get()
    if login.count(' ')>0:
        errorLabel['text']='No spaces are allowed in login'
        return
    if len(login)==0:
        errorLabel['text']='Login cannot be empty'
        return
    with open('users.txt') as file:
        for line in file:
            if line.split(' ')[0]==login:
                errorLabel['text']='This login is taken'
                return
    if len(passwordEntry.get())==0:
        errorLabel['text']='Password cannot be empty'
        return
    password=hashlib.sha3_256(passwordEntry.get().encode()).hexdigest()
    with open('users.txt','a') as file:
        file.write(f'{login} {password}\n')
    errorLabel['text']='Registration successful'

def BtnRegisterSwitch(mode='up'):
    errorLabel['text']=''
    if mode=='up':
        authLabel['text']='Registration'
        btnLogin['text']='Sign up'
        btnLogin['command']=SignUp
        btnRegister['text']='Sign in'
        btnRegister['command']=lambda: BtnRegisterSwitch('in')
        return
    authLabel['text']='Authentication'
    btnLogin['text']='Sign in'
    btnLogin['command']=SignIn
    btnRegister['text']='Sign up'
    btnRegister['command']=BtnRegisterSwitch

def ResultWindowSetup():
    resultWindow.geometry('200x200')

    resultLabel.pack()
    resultText.pack()
    okBtn.pack()

def ReturnToMain(window):
    window.withdraw()
    mainWindow.deiconify()

userData={'login':'','password':''}
activeTest={'id':'','name':'','description':'',
            'questions':[],'answers':[],'answerValues':[]}
testResults=[]

#tests list window
mainWindow=Tk()

mainLabel=Label(mainWindow,text=f'Hello {userData["login"]}')
profileBtn=Button(mainWindow,text='Profile')
testsLabel=Label(mainWindow,text='Tests')
tests=LoadTestsList()
addTestBtn=Button(mainWindow,text='Add new test')

mainWindow.withdraw()

#authentication window
authWindow=Tk()

authLabel=Label(authWindow,text='Authorization')
loginLabel=Label(authWindow,text='Login')
loginEntry=Entry(authWindow)
passwordLabel=Label(authWindow,text='Password')
passwordEntry=Entry(authWindow)
btnLogin=Button(authWindow,text='Sign in',command=SignIn)
errorLabel=Label(authWindow,foreground='#FF0000')
btnRegister=Button(authWindow,text='Sign up',command=BtnRegisterSwitch)

AuthWindowSetup()

#test window
testWindow=Toplevel()
testWindow.withdraw()

testName=Label(testWindow)
testDescription=Label(testWindow)
startTestBtn=Button(testWindow,text='Start test',command=TestPassWindowSetup)
backBtn=Button(testWindow,text='Back',command=lambda: ReturnToMain(testWindow))
questionLabels=[]
answerRadio=[]

TestWindowInitSetup()

#test result window
resultWindow=Tk()
resultWindow.withdraw()

resultLabel=Label(resultWindow,text='Test results:')
resultText=Label(resultWindow)
okBtn=Button(resultWindow,text='ok',command=lambda: ReturnToMain(resultWindow))

ResultWindowSetup()
