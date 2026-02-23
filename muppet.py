import json
from flask import Flask, render_template, request, jsonify, abort, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash
from database_handle import authenticate, change_password, findClasses, findStudentsInClass, getClassName, getResult, getClassId, getStudentName, getAssignmentId, getClassAssignments, addAutomation, getStudentID, getClassAutomations, deleteAutomation, checkAdminAccount, getUserAccounts, getSchoolID, getSchoolClasses, getUserName, addClass, getUserID, deleteClass, addUser, deleteUser, adminOn, adminOff, getPassword, checkRegistered, registerAccount, logAssignment, getAssignmentContent, getMinimumFlagPercentage, setMinimumFlagPercentage, addResult, updateClassName, updateClassUser, removeClassUser, deleteAllUserAutomations, addActivity, getUserActivity, checkAutomation, addContactMessage, addAssignment, getAllResults, getWords, addWords
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
if 1==2:
    print("")



LOAD R1, flag
LOAD R2, False
CMP R1, R2
JNE end
PRINT "Not Found"
JMP start
end:
