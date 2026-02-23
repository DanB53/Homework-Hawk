import json
from flask import Flask, render_template, request, jsonify, abort, session, redirect, url_for, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
from database_handle import authenticate, change_password, findClasses, findStudentsInClass, getClassName, getResult, getClassId, getStudentName, getAssignmentId, getClassAssignments, addAutomation, getStudentID, getClassAutomations, deleteAutomation, checkAdminAccount, getUserAccounts, getSchoolID, getSchoolClasses, getUserName, addClass, getUserID, deleteClass, addUser, deleteUser, adminOn, adminOff, getPassword, checkRegistered, registerAccount, logAssignment, getAssignmentContent, getMinimumFlagPercentage, setMinimumFlagPercentage, addResult, updateClassName, updateClassUser, removeClassUser, deleteAllUserAutomations, addActivity, getUserActivity, checkAutomation, addContactMessage, addAssignment, getAllResults, getWords, addWords,getUserFromClass
from encryption import decrypt
import re
from originalityAPI import aiScan, plScan, aiplScan, plManualUpload, aiManualUpload, aiplManualUpload
from database_interactions import add_dummy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per second"])

@app.errorhandler(404)
def error(e):
    return (render_template('error.html'))

@app.errorhandler(405)
def method_not_allowed(error):
    '''Function to handle method not being allowed
    by redirecting to index page'''
    return redirect('/')


def addWordsProcess(content):
    '''Add the word count to the school statistics
    for the admin to view in the database'''
    schoolID = getSchoolID(user_id=session["user_id"])
    wordCount = len(content.split(" "))
    currentTotal, currentMonthTotal = getWords(schoolID)
    newTotal = currentTotal + wordCount
    newMonth = currentMonthTotal + wordCount
    addWords(schoolID, newTotal, newMonth)

def aiScanProdecure(studentID,assignmentID, content, minFlagPercentage, student, selectedAssignment):
    ''''Function to run the AI scan, add activity to the log and record the result'''
    title, AICertainty = aiScan(studentID[0][0], assignmentID, content)
    if title == "Error":
        '''If there is an error in scanning, log there was an error'''
        addResult(int(studentID[0][0]), int(assignmentID), "ER")
    else:
        '''If the scan is successful, add the words to the scan counter 
        and gather studentID assignmentID'''
        addWordsProcess(content)
        studentID = title.split(",")[0]
        assignmentID = title.split(",")[1]
        '''Determine whether to flag the scan according to user settings
        and store result and activity as such'''
        if AICertainty >= minFlagPercentage:
            addActivity(session["user_id"], student[0] + " " + student[1] + " Tested for AI in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "AI")
        else:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " is clear from AI in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "CL")
def plScanProdecure(studentID,assignmentID, content, minFlagPercentage, student, selectedAssignment):
    ''''Function to run the plagiarism scan, add activity to the log and record the result'''
    minFlagPercentage = getMinimumFlagPercentage(session["user_id"])
    minFlagPercentage = int(minFlagPercentage)/100
    title, PLCertainty = plScan(studentID[0][0], assignmentID, content, minFlagPercentage)
    if title == "Error":
        '''If there is an error in scanning, log there was an error'''
        addResult(int(studentID[0][0]), int(assignmentID), "ER")
    else:
        '''If the scan is successful, add the words to the scan counter 
        and gather certainty, studentID and assignmentID'''
        addWordsProcess(content)
        PLCertainty = int(PLCertainty[:-1]) / 100
        studentID = title.split(",")[0]
        assignmentID = title.split(",")[1]
        '''Determine whether to flag the scan according to user settings
        and store result and activity as such'''
        if PLCertainty >= minFlagPercentage:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " Tested for Plagiarism in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "PL")
        else:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " is clear from Plagiarism in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "CL")
def bothScanProdecure(studentID,assignmentID, content, minFlagPercentage, student, selectedAssignment):
    ''''Function to run the AI and plagiarism scan, add activity to the log and record the result'''
    title, AICertainty, PLCertainty = aiplScan(studentID[0][0], assignmentID, content)
    if title == "Error":
        '''If there is an error in scanning, log there was an error'''
        addResult(int(studentID[0][0]), int(assignmentID), "ER")
    else:
        '''If the scan is successful, add the words to the scan counter and gather certainty, studentID and assignmentID'''
        addWordsProcess(content)
        PLCertainty = int(PLCertainty[:-1]) / 100
        studentID = title.split(",")[0]
        assignmentID = title.split(",")[1]
        '''Determine whether to flag the scan according to user settings 
        and what the scan resulted in and store result and activity as such'''
        if AICertainty >= minFlagPercentage and PLCertainty >= minFlagPercentage:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " Tested for AI and Plagiarism in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "BO")
        elif AICertainty >= minFlagPercentage:
            addActivity(session["user_id"], student[0] + " " + student[1] + " Tested for AI in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "AI")
        elif PLCertainty >= minFlagPercentage:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " Tested for Plagiarism in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "PL")
        else:
            addActivity(session["user_id"],
                        student[0] + " " + student[1] + " is clear from AI and Plagiarism in " + selectedAssignment)
            addResult(int(studentID), int(assignmentID), "CL")

def getDisplayAutomations(classID):
    '''Function to get the automations of a class and format them so the program can
    display them properly to the user'''
    automationList = []
    automations = getClassAutomations(session["user_id"], classID)
    for automation in automations:
        nameTuple = getStudentName(automation[0])
        automationList.append([nameTuple[0][0], nameTuple[0][1], automation[1]])
    return automationList

def getDisplayStudents(classID):
    '''Function to get the students of a class and format them so the program can
    display them properly to the user'''
    studentList = []
    students = findStudentsInClass(classID)
    studentList.append("Add a student")
    for student in students:
        studentList.append(getStudentName(student)[0][0] + " " + getStudentName(student)[0][1])
    return studentList

def getDisplayClasses(schoolID):
    '''Function to get the classes of a school and format them so the program can
    display them properly to the user'''
    classesTuple = getSchoolClasses(schoolID)
    classes = []
    for schoolClass in classesTuple:
        if schoolClass[2] == 0:
            classes.append([schoolClass[1], "None"])
        else:
            classes.append([schoolClass[1], getUserName(schoolClass[2])[0][0]])
    return classes

def getDisplayUsers(schoolID):
    '''Function to get the users of a school and format them so the program can
    display them properly to the user'''
    usersTuple = getUserAccounts(schoolID)
    users = []
    for user in usersTuple:
        result = checkAdminAccount(user[0])
        users.append([getUserName(user[0])[0],result])
    return users

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])





@app.route('/',methods=['GET','POST'])
def index():
    '''Function to process requests to the index page'''
    if request.method == 'POST':
        # Set all cookies to defuault state after the user has accepted cookies
        session["logged_in"] = False
        session["admin_account"] = False
        session["notification"] = "No Notification"
    # Determine whether the user is going on the website for the first time
    try:
        session["logged_in"]
    except:
        # If the cookie does not exist, render the index page with the first time variable set to true
        return render_template("index.html",firstTime="True")
    # If the user has logged in before, render the index page with the first time variable set to false
    session["logged_in"] = False
    session["admin_account"] = False
    session["notification"] = "No Notification"
    return render_template('index.html',firstTime="False")


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5/second")
def login():
    '''Function to process requests to the login page'''
    # If the user has pressed log in, decrypt the information and check to see if the user is registered
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        name, password = json_data['login_details']
        name, password = decrypt(5486416585555566, name), (
            decrypt(5486416585555566, password))

        registered = checkRegistered(getUserID(name))

        # Attempt to authenticate user
        try:
            user_id, result, name = authenticate(name, password)
        except:
            # If credentials are not correct, return a failure to the user
            abort(400)
        if registered == ((b'\x00',),):
            # If the user is not registered, redirect the user to the register page
            return "registerRedirect"
        if result:
            # Set the relevant cookies to the relevant values
            session["logged_in"] = True
            session["user_id"] = user_id
            session["user_name"] = name
            session["admin_account"] = False
            if checkAdminAccount(user_id):
                session["admin_account"] = True
        else:
            # If an error occurs, return a failure to the user
            abort(400)
    return render_template("login.html")



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            storedPassword = getPassword(getUserID(request.form['user_name']))
        except:
            return "loginRedirect"
        authenticate(request.form['user_name'],request.form['tempPassword'])
        if request.form["password"] == request.form["confirm_password"] and (authenticate(request.form['user_name'],request.form['tempPassword']))[1] == True:
            change_password(getUserID(request.form['user_name']),request.form['user_name'],None,request.form['password'],register=True)
            registerAccount(getUserID(request.form['user_name']))
        else:
            return "Passwords must match"
    return render_template("register.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''Function to handle the logout prodecure'''
    try:
        # If the user is not logged in, redirect them to the login page
        if not session["logged_in"]:
            return redirect('/login')
    except:
        # If the user is logged in, redirect them to the index page and reset their cookies
        session['logged_in'] = False
        session["admin_account"] = False
        return redirect('/')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    '''Function to process requests to the contact page'''
    if request.method == 'POST':
        # If adding a new contact message, add it to the database and return success
        if request.form['trigger'] == "newContact":
            addContactMessage(request.form['email'],request.form['message'])
            return "success"
    # If the server is recieving a GET request, render the contact page
    return render_template('contact.html')


@app.route("/help", methods=['GET', 'POST'])
def help():
    '''Function to process requests to the help page'''
    # Render the help page
    return render_template('help.html')


@app.route("/class", methods=['GET', 'POST'])
@app.route("/class/", methods=['GET', 'POST'])
@app.route('/class/<target_class>', methods=['GET', 'POST'])
def classPage(target_class=None):
    '''Function to handle requests to the class page'''
    try:
        # If the user is not logged in, redirect them to the login page
        if not session["logged_in"]:
            return redirect('/login')
    except:
        # If there is an error, redirect them to the index page
        return redirect('/')
    print(target_class)
    selectedAssignment = None
    assignmentID = 0
    if request.method == 'POST':
        trigger = request.form["trigger"]
        if trigger == "student":
            # If the trigger is to scan students, get the relevant variables
            classID = getClassId(user_id=session["user_id"], class_name=target_class)
            selectedStudents = request.form["unmarkedStudents"]
            selectedAssignment = request.form["selectedAssignment"]
            scanType = request.form["scanType"]
            assignmentID = getAssignmentId(selectedAssignment)
            selectedStudents = selectedStudents.split(", ")
            iterCount = 0
            # For every student the user has selected, replace their name with a split 2D list of their first name and last name
            for student in selectedStudents:
                student = student.split(" ")
                selectedStudents[iterCount] = student
                iterCount += 1
            # For every student the user has selected, get their ID, and get the content of their work for that assignment
            for student in selectedStudents:
                studentID = getStudentID(student[0],student[1],classID)
                content = getAssignmentContent(studentID,assignmentID)
                if content == ():
                    # If there is no content, return an error
                    return "No content"
                else:
                    # If the content exists, format the content and get the minimum flag percentage as an int for that user
                    content = content[0][0]
                    minFlagPercentage = getMinimumFlagPercentage(session["user_id"])
                    minFlagPercentage = int(minFlagPercentage) / 100
                    # Call the necessary procedures depending on what method of scanning the user has selected
                    if scanType == "ai":
                        aiScanProdecure(studentID, assignmentID, content, minFlagPercentage, student,selectedAssignment)
                    elif scanType == "pl":
                        plScanProdecure(studentID, assignmentID, content, minFlagPercentage, student,selectedAssignment)
                    elif scanType == "bo":
                        bothScanProdecure(studentID,assignmentID,content,minFlagPercentage, student, selectedAssignment)
        elif trigger == "assignment":
            # If the trigger of the request is to change the assignment, get the assignment ID with the name of the selected assignment
            selectedAssignment = request.form["selectedAssignment"]
            assignmentID = getAssignmentId(selectedAssignment)
    if target_class == None:
        # If the user does not have a selected class, return the base page
        return render_template('class.html')
    # Get the classID of the target class and the students in the class
    classID = getClassId(user_id=session["user_id"], class_name=target_class)
    studentsTuple = findStudentsInClass(classID)
    students_results = []
    # For every student in the class, get their first name, last name and the result of their work. If unmarked, set the result to be "UN"
    for i in studentsTuple:
        studentName = getStudentName(i)
        firstName = studentName[0][0]
        lastName = studentName[0][1]
        result = getResult(assignmentID,i)
        if result:
            resultStatus = result[0][0]
        else:
            resultStatus = "UN"
            # If there is no work for the student, set the result status to be none
            if getAssignmentContent(i, assignmentID) == ():
                resultStatus = "None"
        # Append the first name, last name and result status to the students_results list.
        students_results.append([f"{firstName} {lastName}", resultStatus])
    # Get the assignments in the class and format them correctly to be rendered on the page
    assignments = getClassAssignments(classID)
    assignments = [f"{assignments[i][0]}" for i in range(len(assignments))]
    if selectedAssignment == None:
        # If there is no selected assignment, set the selected assignment as a prompt to select an assignment
        selectedAssignment="Select An Assignment"
        return render_template('class.html', classname=target_class,
                               selectedAssignment=selectedAssignment, assignments=assignments)
    # Return the HTML for students to replace the students div with (allows for jinja 2 rendering)
    return render_template('students.html', students=students_results)






@app.route('/profile', methods=['GET', 'POST'])
def profilePage():
    '''Function to handle requests to the profile page'''
    try:
        # If the user is not logged in, send them to the login page
        if not session["logged_in"]:
            return redirect('/login')
    except:
        # If the cookie does not exist, send them to the index page
        return redirect('/')


    if request.method == "POST":
        if request.form["trigger"] == "options":
            # If the trigger of the request is to change passwords, get the values entered. If an error occurs, return an error
            try:
                enteredOldPassword = request.form['profilePasswordBox1']
                enteredChangePassword = request.form['profilePasswordBox2']
                enteredConfirmPassword = request.form["profilePasswordBox3"]
                if enteredChangePassword == enteredConfirmPassword:
                    # If the entered and confirm passwords match, run the change password function, and get them to log back in
                    if change_password(session["user_id"],session["user_name"],enteredOldPassword,enteredChangePassword):
                        return redirect(url_for("login"))
                    else:
                        return abort(400)
                else:
                    # If the entered and confirm passwords dont match, return an error
                    return abort(400)
            except:
                abort(400)
        elif request.form["trigger"] == "classChange" and request.form["selectedClass"] != "Please select a class":
            # If the user has changed the class and it is not to the prompt to select a class in the drop down menu
            # Get the automations of the user, and fetch the list of students in a class to be added to the drop down menu to add a new automation for a student
            classID = getClassId(user_id=session["user_id"],class_name=request.form["selectedClass"])
            studentList = getDisplayStudents(classID)
            automationList = getDisplayAutomations(classID)
            # Return the HTML file to replace the automations div on the profile page, allowing for jinja2 formatting to be rendered
            return render_template("automations.html", students=studentList, existingAutomations=automationList)
        elif request.form["trigger"] == "addAutomation":
            # If the user has submitted adding an automation, get the class ID, automations for that class ID and the IDs of the students
            classID = getClassId(user_id=session["user_id"],class_name=request.form["selectedClass"])
            automations = getClassAutomations(session["user_id"], classID)
            ids = getStudentID(request.form["selectedStudent"].split()[0],request.form["selectedStudent"].split()[1],classID)
            # Check to see if there is already an automation for the student entered
            for id in ids:
                for automation in automations:
                    if automation[0] == id[0]:
                        # If there is already an automation for that student, return an error to be handled client side
                        abort(400)
            # Add the automation, get class students and automations and return the automations html page to replace the automations div on the page (allows for jinja 2 rendering)
            addAutomation(session["user_id"],getStudentID(request.form["selectedStudent"].split()[0],request.form["selectedStudent"].split()[1],classID),classID,request.form["selectedOption"])
            studentList = getDisplayStudents(classID)
            automationList = getDisplayAutomations(classID)
            return render_template("automations.html", students=studentList, existingAutomations=automationList)
        elif request.form["trigger"] == "deleteAutomation":
            # If the user presses the option to delete an automation,
            # Add the automation, get class students and automations and return the automations html page to replace the automations div on the page (allows for jinja 2 rendering)
            classID = getClassId(user_id=session["user_id"],class_name=request.form["selectedClass"])
            deleteAutomation(session["user_id"],getStudentID(request.form["first_name"],request.form["last_name"],classID),classID,request.form["scan_type"])
            studentList = getDisplayStudents(classID)
            automationList = getDisplayAutomations(classID)
            return render_template("automations.html", students=studentList, existingAutomations=automationList)
        elif request.form["trigger"] == "changeMinimumFlag":
            # If the user changes their minimum flag percentage, change the minimum flag percentage
            setMinimumFlagPercentage(session["user_id"],request.form["newValue"])

    # Get all the users classes and add them to a list
    classesTuple = findClasses(session["user_id"])
    classes = []
    for _, className in classesTuple:
        classes.append(className)
    # Get the users minimum flag percentage and render the html page
    minFlagPercentage = getMinimumFlagPercentage(session["user_id"])
    return render_template('profile.html', selectedClass="Please select a class",classes=classes,minFlagPercentage=minFlagPercentage)


@app.route('/home', methods=['GET', 'POST'])
def homePage():
    '''Function to handle requests to the home page'''
    try:
        # If the user is not logged in, return them to the log in page
        if not session["logged_in"]:
            return redirect('/login')
    except:
        # If the cookie doesn't exist, send them to the index page
        return redirect('/')
    if request.method == "POST":
        trigger = request.form["trigger"]
        if trigger == "manualUpload":
            # If the user has triggered a manual upload, get the necessary values
            text = request.form["text"]
            option = request.form["option"]
            minFlagPercentage = getMinimumFlagPercentage(session["user_id"])
            # If the user selects plagiarism, run the plagiarism scan
            if option == "pl":
                result = plManualUpload(session["user_id"], text, minFlagPercentage)
                # If the scan result is plagiarism, log the activity
                if result == "Pl":
                    addActivity(session["user_id"],"Your scan tested positive for Plagiarism")
                # If the scan is less than 50 words, return an error
                elif result == "Error":
                    return "Scan must be min 50 words"
                # If the scan is clear, log the activity
                else:
                    addActivity(session["user_id"],"Your scan is clear from Plagiarism")
            # If the user selects plagiarism, run the plagiarism scan
            elif option == "ai":
                result = aiManualUpload(session["user_id"], text)
                # If the scan is not at least 50 words, return an error
                if result == "Error":
                    return "Scan must be min 50 words"
                # Check if the result percentage is sufficient to flag depending on the flag percentage
                minFlagPercentage =int(minFlagPercentage)/100
                if result >= minFlagPercentage:
                    addActivity(session["user_id"], "Your scan tested positive for AI")
                else:
                    addActivity(session["user_id"], "Your scan is clear from AI")
            # If the user selects to scan both plagiarism and AI, run the AI and plagiarism scans
            elif option == "plai":
                aiResult, plResult = aiplManualUpload(session["user_id"], text)
                # If the scan is not at least 50 words, return an error
                if aiResult == "Error":
                    return "Scan must be min 50 words"
                # Check to see if the results should be flagged, and add the relevant activity
                aiResult = int(aiResult)
                plResult = int(plResult[:-1])/100
                if aiResult >= minFlagPercentage and plResult >= minFlagPercentage:
                    addActivity(session["user_id"], "Your scan tested positive for AI and Plagiarism")
                elif aiResult >= minFlagPercentage:
                    addActivity(session["user_id"], "Your scan tested positive for AI")
                elif plResult >= minFlagPercentage:
                    addActivity(session["user_id"], "Your scan tested positive for Plagiarism")
                else:
                    addActivity(session["user_id"], "Your scan is clear from AI and Plagiarism")
            # Get and return the user activities html to replace the activities div on the home page
            activities = getUserActivity(session["user_id"])
            activities.reverse()
            return render_template("activities.html",activities=activities)
    # Get the users classes and activities, and render the home page with those values
    classesTuple = findClasses(session["user_id"])
    classes = []
    for _, className in classesTuple:
        classes.append(className)
    activities = getUserActivity(session["user_id"])
    activities.reverse()
    return render_template('home.html',
                           classes=classes, activities=activities)

@app.route("/classes", methods=['GET', 'POST'])
def classes():
    '''Function to handle requests to the classes page'''
    try:
        # If the account is not logged in, redirect to the login page
        if not session["logged_in"]:
            return redirect('/login')
    # If the cookie does not exist, return the user to the index page
    except:
        return redirect('/')
    # Get the users classes
    classesTuple = findClasses(session["user_id"])
    classes = []
    for _, className in classesTuple:
        classes.append(className)
    # If there is no classes in the list, add an error message to show to the user
    if classes == []:
        classes=["No classes found. Ask your administrator to add you to a class."]
    # Render the classes page with the users classes
    return render_template("classes.html", classes=classes)



@app.route("/admin", methods=['GET', 'POST'])
def admin():
    '''Function to handle requests to the admin page'''
    try:
        # If the user is not an admin, set the cookie to false and redirect them to the home page
        if not checkAdminAccount(session["user_id"]):
            session["admin_account"] = False
            # If the request is a post method and the user isnt an admin, redirect them to the login page
            if request.method == "POST":
                return "Redirect to log in."
            return redirect(url_for("homePage"))
    except:
        # If the cookie doesn't exist, redirect the user to the index page
        return redirect(url_for("index"))
    # Get the schoolID which is used throughout the function
    schoolID = getSchoolID(session["user_id"])
    if request.method == "POST":
        if request.form["trigger"] == "newClass":
            # If the request is to add a new class, get the userID entered if the user doesn't exist, return an error
            try:
                userID = getUserID(request.form["userName"])
            except:
                abort(400)
            # If there is a further error, don't add the class
            if userID == ():
                return "Cannot add class - user not found."
            # Add a class, and render the classes part of the admin page with the new list of classes
            addClass(request.form["className"],schoolID,userID)
            classes = getDisplayClasses(schoolID)
            return render_template("admin-classes.html", classes=classes)

        elif request.form["trigger"] == "removeClass":
            # If the user tries to remove the class, authenticate the user
            try:
                userID = getUserID(request.form["userName"])
            except:
                abort(400)
            # If the user exists, delete the class and return the class part of the admin page
            deleteClass(getClassId(user_id=userID,class_name=request.form["className"]))
            classes = getDisplayClasses(schoolID)
            return render_template("admin-classes.html", classes=classes)
        elif request.form["trigger"] == "newUser":
            # If the user adds a new class, check to see if the user being added should be an admin or not
            adminAccount = False
            if request.form["adminAccount"] == "true":
                adminAccount = True
            # Add the user
            result = addUser(schoolID, request.form["userName"],generate_password_hash(request.form["tempPassword"]),adminAccount)
            # If the function returns that the user already exists, inform the user of the error
            if result == "User Exists":
                return "Error: User already exists"
            # Get the users of the school and display them to the user
            users = getDisplayUsers(schoolID)
            return render_template("admin-users.html", users=users)
        elif request.form["trigger"] == "removeUser":
            # If the user removes a user, get the ID of the user to delete and remove all information associated with the user
            userID = getUserID(request.form["userName"])
            removeClassUser(userID)
            deleteAllUserAutomations(userID)
            deleteUser(userID)
            # Get all the users of the class and return them to the user
            users = getDisplayUsers(schoolID)
            return render_template("admin-users.html", users=users)
        elif request.form["trigger"] == "adminOn":
            # If the user toggles a user to be an admin, set them to an admin and return the users to the user
            adminOn(getUserID(request.form["userName"]))
            users = getDisplayUsers(schoolID)
            return render_template("admin-users.html", users=users)
        elif request.form["trigger"] == "adminOff":
            # If the user toggles a user to get rid of their admin status, check to see if the user is trying to remove themselves as an admin
            if getUserName(session["user_id"])[0][0] == request.form["userName"]:
                # Tell the user they cannot remove themselves as admin
                return "You cannot remove yourself as an admin."
            # If allowed, remove the user selected as an admin
            adminOff(getUserID(request.form["userName"]))
            # Get all the users of the class and return them to the user
            users = getDisplayUsers(schoolID)
            return render_template("admin-users.html", users=users)
        elif request.form["trigger"] == "changeClassName":
            # If the user changes a class name, change the class name
            updateClassName(getClassId(request.form["oldClassName"],getUserID(request.form["userName"]),schoolID),request.form["newClassName"])
            # Get the classes of the school and display them to the user
            classes = getDisplayClasses(schoolID)
            return render_template("admin-classes.html", classes=classes)
        elif request.form["trigger"] == "changeClassUser":
            try:
                oldUserID = getUserID(request.form["oldUserName"])[0][0]
            except:
                oldUserID = 0
            try:
                classID = getClassId(request.form["newClassName"],oldUserID,schoolID)[0][0]
            except:
                classID = getClassId(request.form["oldClassName"], oldUserID, schoolID)
            try:
                newUserID = getUserID(request.form["newUserName"])[0][0]
            except:
                return "That user does not exist."
            updateClassUser(classID, newUserID)
            classes = getDisplayClasses(schoolID)
            return render_template("admin-classes.html", classes=classes)
    classes = getDisplayClasses(schoolID)
    users = getDisplayUsers(schoolID)
    allResults = getAllResults(schoolID)
    totalAI = 0
    totalPL = 0
    totalBO = 0
    totalCL = 0
    totalScans = 0
    for result in allResults:
        totalScans += 1
        result = result[0]
        if result == "AI":
            totalAI += 1
        elif result == "PL":
            totalPL += 1
        elif result == "BO":
            totalBO += 1
        elif result == "CL":
            totalCL += 1
    try:
        totalAI = round(totalAI/totalScans * 100,2)
    except:
        totalBO = 0
    try:
        totalCL = round(totalCL/totalScans * 100,2)
    except:
        totalCL = 0
    try:
        totalPL = round(totalPL/totalScans * 100,2)
    except:
        totalPL = 0
    try:
        totalBO = round(totalBO/totalScans * 100,2)
    except:
        totalBO = 0
    try:
        totalWords, monthWords = getWords(schoolID)
    except:
        totalWords = 0
        monthWords = 0
    amountSpent = monthWords * 0.0004
    return render_template("admin.html", classes=classes, users=users, totalWords=totalWords, monthWords=monthWords, amountSpent=amountSpent, totalAI=totalAI, totalPL=totalPL, totalBO=totalBO, totalCL=totalCL)




@app.route("/api/assignment", methods=["GET","POST"])
def apiAssignment():
    content = request.get_json()
    studentName = content["name"]
    schoolName = content["school name"]
    className = content["class name"]
    assignmentName = content["assignment name"]
    assignmentContent = content["assignment content"]
    firstName, lastName = studentName.split(" ")
    classID = getClassId(class_name=className, school_id=getSchoolID(school_name=schoolName))[0][0]
    studentID = getStudentID(firstName,lastName,classID)
    assignmentID = getAssignmentId(assignmentName)
    assignmentContent = re.sub("[\u200e\u200f\u202a-\u202e]","",assignmentContent)
    assignmentContent = assignmentContent.replace('"','\"')
    try:
        logAssignment(studentID[0][0],assignmentID,str(assignmentContent).encode("UTF-8"))
    except:
        addAssignment(assignmentName,classID)
        assignmentID = getAssignmentId(assignmentName)
        logAssignment(studentID,assignmentID,str(assignmentContent).encode("UTF-8"))
    runScan = checkAutomation(studentID[0][0], classID)
    if runScan != ():
        try:
            userID = getUserFromClass(classID)
            minFlagPercentage = getMinimumFlagPercentage(userID)
            minFlagPercentage = int(minFlagPercentage) / 100
            if runScan[0][0] == "AI":
                aiScanProdecure(studentID, assignmentID,assignmentContent,minFlagPercentage,[firstName,lastName],assignmentName)
            elif runScan[0][0] == "Plagiarism":
                plScanProdecure(studentID, assignmentID,assignmentContent,minFlagPercentage,[firstName,lastName],assignmentName)
            elif runScan[0][0] == "Both":
                bothScanProdecure(studentID, assignmentID,assignmentContent,minFlagPercentage,[firstName,lastName],assignmentName)
        except:
            return "Error"
    return "Success"



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
