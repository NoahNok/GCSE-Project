import csv

mQ = []
gQ = []
currentUser = ""
def checkFilesExist():
    # Each with will create the file if it doesnt exist otherwise it will leave it.
    with open("userdata.csv", "a") as file:
        file.close()
    with open("testdata.csv", "a") as file:
        file.close()
    with open("gQ.txt", "a") as file:
        file.close()
    with open("mQ.txt", "a") as file:
        file.close()


def loadQuestions():
    # Loads questions from files into lists
    with open("gQ.txt", "r") as geoQ, open("mQ.txt", "r") as matQ:
        for gl in geoQ:
            gQ.append(gl)
        for ml in matQ:
            mQ.append(ml)
    

            


def newUser():
    # Ask for name, age password
    user = input("Username: ")
    age = input("Age: ")
    password = input("Password: ")
    # Generates account details
    username = user[:3]+age
    with open('userdata.csv', 'rt') as f:
     reader = csv.reader(f, delimiter=',')
     for row in reader:
          if username == row[0]: 
              print("Name taken! - " + username)
              return
              
    
    with open("userdata.csv", "a") as file:

        file.write(username+","+password+","+age+"\n")

def login():
    # Simple login
    username = input("Username: ")
    password = input("Password: ")
    with open('userdata.csv', 'rt') as f:
        # Reads file
        reader = csv.reader(f, delimiter=',')
        # Read file and split to read per cell into a list
        for row in reader:
            # Loop through list to see if username matches
            if (username == row[0]):
                # If the username matches we get the next cell along and see if the password matches
                if (password == row[1]):
                    print("Correct Details")
                    # Set the global current user to be used for saving and data managment later
                    global currentUser
                    currentUser  = username
                    logedInRun()
                    return
                else:
                    print("Correct User, Wrong Password")
                    # Notify they had the correct username but they used the wrong password!
                    return
            
        print("No user found!")

def numbToLetter(numb):
    # Returns a letter for a question via the question number
    if (numb == 0):
        return "A: "
    if (numb == 1):
        return "B: "
    if (numb == 2):
        return "C: "
    else:
        return "D: "

def formatQuestion(question, anwCount):
    # Basic formater to send questions to the user
    Q = question.split(",")
    # Questions is a string controled with commas. We split to get 5 items, Question and 4 Anwsers
    availableAnwsers = Q[0] + ": "
    tempCount = 0
    for i in Q[1:]:
        # LOOPS UNTIL THE CORRECT AMOUNT OF ANWSERS ARE INCLUDED
        if (tempCount == anwCount):
            break
        availableAnwsers += str(numbToLetter(tempCount)) + i + " "
        tempCount += 1
        

    return availableAnwsers
    

def toPercent(score, questions):
    # Turns results in to a percentage rounded to 2d.p
    return str(round((score/questions)*100, 2))


def takeMathsQuiz(diff):
    correct = 0;
    totalQ = len(mQ)
    # Loop throught all available questions
    for i in range(len(mQ)):
        print(i)
        if (diff == "E"):
            # Prints the question formated properly with the right amount of options
            print(formatQuestion(mQ[i], 2))
        if (diff == "M"):
            print(formatQuestion(mQ[i], 3))

        if (diff == "H"):
            print(formatQuestion(mQ[i], 4))

        # Input selection, takes any character or number, if you give andthing other than the anwser you will get the question wrong!
        anwser = input ("Anwser: A-D (If C or D are not valid and yo utype the letter you will get the question wrong! ")
        if (anwser.upper() == "A"):
            # Forces to upper to prevent errors

            
            correct += 1
            if (correct != totalQ):
                print("Correct, next question!")
            else:
                print("Correct!")
        else:
            print("Incorrect! Better luck next time!")

    test = "Ma_" + diff
    print("Quiz over ("+test+"), Score: " + str(correct) + "/" + str(totalQ) +"")
    location = 0
    foundUser = False
    tempData = []
    # Saves data to file
    with open("testdata.csv", "rt") as file:
        reader = csv.reader(file, delimiter='\n')
        # Take every row of data from the file and add it to the list
        for row in reader:
            tempData.append(row[0])

        # We re-read the file but split on every cell in each row
        r = csv.reader(open("testdata.csv", "r"), delimiter=',')
        for row2 in r:
            
            
            if (row2[0] == currentUser):
                # Fires if the file already contains data for that person, deciding wether to rewrite with extra data or make the current user a new data section
                foundUser = True
                break
            # Marks the row index which is equivalent too the index of that users information in the tempData list
            location += 1
            
    # Check if the user was found from the loop
    if (foundUser == False):
        # Append to add a new user to the data list and add there test result
        with open("testdata.csv", "a") as f:
            f.write(currentUser + "," + test+":["+str(correct)+"/"+str(totalQ)+"]:"+str(round((correct/totalQ)*100,2)))
    
    else:
        # Write the file again with updated data for the student
        with open("testdata.csv", "w") as file:
            # Using our index location we can find the current data for that user and then reset it to itself and the extra data
            tempData[location] = tempData[location]+","+test+":["+str(correct)+"/"+str(totalQ)+"]:"+str(round((correct/totalQ)*100,2))
            # Loop to write all the data back to the file
            for line in tempData:
                file.write(line+"\n")




        
def readRow(row):
    
    elementList = str(row).split(":")
    test = elementList[0]
    score = elementList[1]
    perc = elementList[2]
    return (test +"   | " + score + "  | " + perc+ "        | ")

def subjectData(sub, diff):
    with open("testdata.csv", "r") as data:
        reader = csv.reader(data)
        highestPerc = 0
        highestUser = ""
        avgPer = 0
        totalPerc = 0
        testsDone = 0
        for row in reader:
            for i in row:
                splt = i.split(":")
                if (splt[0] == sub+"_"+diff):
                    print(row[0] + " Test: " + sub+"_"+diff + " Score: " + splt[2])
                    if (float(splt[2]) > highestPerc):
                        highestPerc = float(splt[2])
                        highestUser = row[0]
                    totalPerc += float(splt[2])
                    testsDone += 1
        print("Highest Scorer: " + highestUser + " with: " + str(highestPerc)+"%")
        print("Average %: " + str(round(totalPerc/testsDone, 2)))

    

def getReport(type):
    if (type == "1"):
        existed = False;
        user = input("Please provide the users Username (Will be the first 3 letters of their name followed bu their age! First Letter Capitalised!): ")
        with open("testdata.csv", "r") as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                if (row[0] == user):
                    existed = True
                    print("Test   | Score  | Percentage  | Grade")
                    for subrow in row[1:]:
                        print(readRow(subrow))
            if (existed == False):
                print("That user does not exist or had no data!")

    if (type == "2"):
        
            subject = input("What Subject? Geography (Ge), Maths (Ma) or English (En)? ")
            difficulty = input("What difficulty? (E|M|H): ")
            if (difficulty == "E" or difficulty == "M" or difficulty == "H"):
                if (subject == "Ge" or subject == "Ma" or subject == "En"):
                    return subjectData(subject, difficulty)

       
    
              


        
    

          
    




    
                
def logedInRun():
    # Only runs when you login
    while True:
        # Invalid option gets ignored and asks you again, case sensitive
        option = input("Lets take a test! There are 3 Options: Geogrpahy, Maths and English (G,M,E) or you can view results or generate a report!: (V/R)? ")
        if (option == "M"):
            diff = input("Difficulty: Easy, Medium, Hard (E,M,H)? ")
            if (diff == "E"):
                takeMathsQuiz("E")
            if (diff == "M"):
                takeMathsQuiz("M")
            if (diff == "H"):
                takeMathsQuiz("H")
            else:
                # Basic error check
                print("Thats not a valid difficulty!")

        if (option == "R"):
            reportType = input("There are two report types! View results for a username (1) or View all results for a subject and difficulty (2)")
            if (reportType == "1"):
                getReport("1")
            if (reportType == "2"):
                getReport("2")
            else:
                "Invalid report type! Please try again!"
                
        
                



def run():
    checkFilesExist()
    loadQuestions()
    while True:
        # Input what the user wants to do from two choices
        option = input("New User N or Login L")
        if (option == "N"):
            newUser()



        if (option == "L"):
            login()

        # If neither are selected then ask again




# Starts the main loop
run()
