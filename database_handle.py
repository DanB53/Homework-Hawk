import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


def getPassword(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getPassword(%s)", (user_id))
    row = cursor.fetchone()
    return row

def authenticate(entered_name, entered_password):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    try:
        cursor.execute("CALL getUser(%s)", (entered_name))
        row = cursor.fetchone()
        userID, password = row
    except:
        return False
    if check_password_hash(password, entered_password):
        return userID, True, entered_name
    # elif
    else:
        return False
def change_password(id, entered_name, entered_old_password, new_password, register=False):
    if register==True or authenticate(entered_name, entered_old_password)[1] == True:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        new_password = generate_password_hash(new_password)
        cursor.execute("CALL changePassword(%s,%s)", (id,new_password))
        connection.commit()
        return True

    else:
        return False

def findClasses(id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL findClasses(%s)", (id))
    row = cursor.fetchall()
    return(row)

def findStudentsInClass(class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL findStudentsInClass(%s)", (class_id))
    row = cursor.fetchall()
    values = []
    for i in row:
        values.append(i[0])
    return (values)

def getClassId(class_name, user_id=None, school_id=None):
    if user_id is not None:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL getClassID(%s,%s)", (user_id, class_name))
        row = cursor.fetchall()
        return (row)
    elif school_id is not None:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL getClassIDWithSchoolID(%s,%s)", (school_id, class_name))
        row = cursor.fetchall()
        return (row)

def getAssignmentId(assignmentName):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getAssignmentId(%s)", (assignmentName))
    row = cursor.fetchall()
    try:
        row = row[0][0]
        row = int(row)
    except:
        row = None

    return (row)

def getClassName(class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getClassName(%s)", (class_id))
    row = cursor.fetchall()
    return(row)

def getStudentName(student_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getStudentName(%s)", (student_id))
    row = cursor.fetchall()
    return(row)

def getStudentID(first_name, last_name, class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getStudentID(%s,%s,%s)", (first_name, last_name, class_id))
    row = cursor.fetchall()
    return(row)

def getResult(assignment_id, student_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getResult(%s,%s)", (assignment_id, student_id))
    row = cursor.fetchall()
    return(row)

def getClassAssignments(class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getClassAssignments(%s)", (class_id))
    row = cursor.fetchall()
    return(row)

def addAutomation(user_id, target_student_id, target_class_id, target_scanType):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    try:
        cursor.execute("CALL addAutomation(%s,%s,%s,%s)", (target_student_id, target_class_id, target_scanType,user_id))
        connection.commit()
        return "Success"
    except:
        return "Error"


def deleteAutomation(user_id, target_student_id, target_class_id, target_scanType):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    try:
        cursor.execute("CALL deleteAutomation(%s,%s,%s,%s)", (target_student_id, target_scanType, target_class_id ,user_id))
        connection.commit()
        return "Success"
    except:
        return "Error"

def getClassAutomations(user_id, target_class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getClassAutomations(%s,%s)", (user_id, target_class_id))
    row = cursor.fetchall()
    return(row)

def checkAdminAccount(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL checkAdminStatus(%s)", (user_id))
    row = cursor.fetchall()
    row = str(row[0][0])
    row = row[-2]
    if row == "1":
        row = True
    else:
        row = False
    return(row)

def getUserAccounts(school_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getUserAccounts(%s)", (school_id))
    row = cursor.fetchall()
    return (row)


def getSchoolClasses(school_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getSchoolClasses(%s)", (school_id))
    row = cursor.fetchall()
    return (row)

def getSchoolID(user_id=None, school_name=None):
    if user_id is not None:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL getSchoolID(%s)", (user_id))
        row = cursor.fetchall()
        return (row)
    elif school_name is not None:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL getSchoolIDWithName(%s)", (school_name))
        row = cursor.fetchall()
        return (row)
def getUserName(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getUserName(%s)", (user_id))
    row = cursor.fetchall()
    return (row)

def addClass(name, school_id, user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL addClass(%s, %s, %s)", (school_id, name, user_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)

def getUserID(name):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getUserID(%s)", (name))
    row = cursor.fetchall()
    return (row)

def deleteClass(class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL deleteClass(%s)",(class_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)

def addUser(school_id, name, temp_password, admin_account):
    # Check if the user already exists
    if getUserID(name) != ():
        return "User Exists"

    # Convert the admin_account to an integer for MySQL (1 for True, 0 for False)
    admin_account_value = "true" if admin_account else "false"

    try:
        # Establish database connection
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="1",
            database="hh_db"
        )
        cursor = connection.cursor()

        # Extract school_id if it's wrapped in a tuple
        if isinstance(school_id, (list, tuple)) and len(school_id) > 0:
            school_id = school_id[0][0]

        # Execute the stored procedure
        cursor.execute(
            "CALL addUser(%s, %s, %s, %s)", 
            (school_id, name, temp_password, admin_account_value)
        )
        
        # Fetch the results (if any)
        row = cursor.fetchall()

        # Commit the transaction
        connection.commit()

        return row

    except pymysql.MySQLError as e:
        # Handle any MySQL errors
        print( f"MySQL Error: {str(e)}")

def deleteUser(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL deleteUser(%s)",(user_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)

def adminOn(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL adminOn(%s)",(user_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)

def adminOff(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL adminOff(%s)",(user_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)


def checkRegistered(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL checkRegistered(%s)", (user_id))
    row = cursor.fetchall()
    return (row)


def registerAccount(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL registerAccount(%s)",(user_id))
    row = cursor.fetchall()
    connection.commit()
    return (row)


def checkLoggedAssignment(student_id,assignment_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL checkLoggedAssignment(%s,%s)",(student_id, assignment_id))
    row = cursor.fetchall()
    if row == ():
        return "good"
    else:
        return "bad"

def logAssignment(student_id,assignment_id, assignment_content):
    if checkLoggedAssignment(student_id, assignment_id) == "good":
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db",charset='utf8mb4')
        cursor = connection.cursor()
        cursor.execute("CALL logAssignment(%s,%s,%s)", (student_id, assignment_id, assignment_content))
        row = cursor.fetchall()
        connection.commit()
        return (row)
    else:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db",charset='utf8mb4')
        cursor = connection.cursor()
        cursor.execute("CALL updateAssignmentContent(%s,%s,%s)", (student_id, assignment_id, assignment_content))
        row = cursor.fetchall()
        connection.commit()
        return (row)

def getAssignmentContent(student_id, assignment_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getAssignmentContent(%s,%s)",(student_id, assignment_id))
    row = cursor.fetchall()
    return row


def getMinimumFlagPercentage(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getMinimumFlagPercentage(%s)", (user_id))
    row = cursor.fetchall()
    return row[0][0]

def setMinimumFlagPercentage(user_id, newPercentage):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL setMinimumFlagPercentage(%s,%s)",(user_id, newPercentage))
    connection.commit()
    row = cursor.fetchall()
    return row

def addResult(student_id, assignment_id, result):
    if getResult(assignment_id, student_id) == ():
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL addResult(%s,%s,%s)",(student_id, assignment_id, result))
        connection.commit()
        row = cursor.fetchall()
        return row
    else:
        host, connectionUser, connectionPassword = "localhost", "root", "1"
        connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
        cursor = connection.cursor()
        cursor.execute("CALL updateResult(%s,%s,%s)",(student_id, assignment_id, result))
        connection.commit()
        row = cursor.fetchall()
        return row

def updateClassName(class_id, name):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL updateClassName(%s,%s)", (class_id, name))
    connection.commit()
    row = cursor.fetchall()
    return row

def updateClassUser(class_id, new_user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL updateClassUser(%s,%s)", (class_id, new_user_id))
    connection.commit()
    row = cursor.fetchall()
    return row

def removeClassUser(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL removeClassUser(%s)", (user_id))
    connection.commit()
    row = cursor.fetchall()
    return row


def deleteAllUserAutomations(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL deleteAllUserAutomations(%s)", (user_id))
    connection.commit()
    row = cursor.fetchall()
    return row

def addActivity(user_id, activity_text):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL addActivity(%s,%s)", (user_id,activity_text))
    connection.commit()
    row = cursor.fetchall()
    return row

def getUserActivity(user_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getUserActivity(%s)", (user_id))
    row = cursor.fetchall()
    activities = []
    for activity in row:
        activities.append(activity[0])
    return activities


def checkAutomation(student_id, class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL checkAutomation(%s,%s)", (student_id, class_id))
    row = cursor.fetchall()
    return row

def addContactMessage(email, message):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL addContactMessage(%s,%s)", (email, message))
    connection.commit()
    row = cursor.fetchall()
    return row

def addAssignment(name, class_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL addAssignment(%s,%s)", (name, class_id))
    connection.commit()
    row = cursor.fetchall()
    return row

def getAllResults(school_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getAllResults(%s)", (school_id))
    row = cursor.fetchall()
    return row

def getWords(school_id):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getWords(%s)", (school_id))
    row = cursor.fetchall()
    return row[0]

def addWords(school_id, newTotal, newMonth):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL addWords(%s,%s,%s)", (school_id, newTotal, newMonth))
    connection.commit()
    row = cursor.fetchall()
    return row


def getUserFromClass(targetClassID):
    host, connectionUser, connectionPassword = "localhost", "root", "1"
    connection = pymysql.connect(host=host, user=connectionUser, password=connectionPassword, database="hh_db")
    cursor = connection.cursor()
    cursor.execute("CALL getClassUserID(%s)", (targetClassID))
    row = cursor.fetchall()
    return row[0]