#TO DO:
 # Change flowchart ChangeSchool function to include current school and new school


function authenticate(hashedInput)
    userLogins = db(userLogins)
    for value in userLogins
        if value.hash == hashedInput
            return "Authenticated"
        else
            return "Not Authenticated"
        endif
    endfor
endfunction






function addWork(studentName, assignmentName, school)
    try
        assignments = db(assignments)
        assignments.add(studentName, assignmentName,school)
        return "Successfully added assignment"
    except
        return "Failed to add assignment"
endfunction
