function removeClass(classInfo){
    if (confirm("Are you sure you want to delete the class "+classInfo[0]+"?\nThis cannot be undone.")){
        $.ajax({
             type: 'POST',
             url: '/admin',
             data: {
                 trigger:"removeClass",
                 className: classInfo[0],
                 userName: classInfo[1]
             },
            success: function(data) {
                var classes = document.querySelector("#classes");
                classes.innerHTML = data
                }
            });
    }
};

function removeUser(userName){
    if (confirm("Are you sure you want to delete "+userName+" as a user?\nThis cannot be undone.")){
        $.ajax({
             type: 'POST',
             url: '/admin',
             data: {
                 trigger:"removeUser",
                 userName: userName
             },
            success: function(data) {
                var users = document.querySelector("#users");
                users.innerHTML = data
                }
            });
    }
};

function adminOn(userName){
    if (confirm("Are you sure you want to make "+userName+" an admin?")){
            $.ajax({
                 type: 'POST',
                 url: '/admin',
                 data: {
                     trigger:"adminOn",
                     userName: userName
                 },
                success: function(data) {
                    var users = document.querySelector("#users");
                    users.innerHTML = data
                    }
                });
        }
}

function adminOff(userName){
    if (confirm("Are you sure you want to remove "+userName+" as an admin?")){
            $.ajax({
                 type: 'POST',
                 url: '/admin',
                 data: {
                     trigger:"adminOff",
                     userName: userName
                 },
                success: function(data) {
                     if(data === "Redirect to log in."){
                      document.location.href = "/home"
                     }
                     else if (data !== "You cannot remove yourself as an admin."){
                         var users = document.querySelector("#users");
                         users.innerHTML = data
                    }

                    else{
                        document.getElementById("notification-text").innerText = "You cannot remove yourself as an admin.";
                        notify(2)
                    }
                }});
        }
}

$(document).on("submit","#newClass",function (event){
    event.preventDefault();
    var className =  $("#newClassName").val()
    var userName =  $("#classUserName").val()
    $.ajax({
         type: 'POST',
         url: '/admin',
         data: {
             trigger:"newClass",
             className: className,
             userName: userName
         },
        success: function(data) {
            if (data === "Cannot add class - user not found."){
                document.getElementById("notification-text").innerText = "Cannot add class - user not found.";
                 notify(3)
            }
            else{
                var classes = document.querySelector("#classes");
                classes.innerHTML = data
            }
            }
        });
});

$(document).on("submit","#newUser",function (event){
    event.preventDefault();
    var userName =  $("#newUserName").val()
    var tempPassword =  $("#tempPassword").val()
    var adminAccount = $("#adminAccountCheckbox").is(":checked")
    $.ajax({
         type: 'POST',
         url: '/admin',
         data: {
             trigger:"newUser",
             userName: userName,
             adminAccount:adminAccount,
             tempPassword:tempPassword
         },
        success: function(data) {
             if (data === "Error: User already exists"){
                 document.getElementById("notification-text").innerText = "That user already exists.";
                 notify(2)
             }
             else{
                 var classes = document.querySelector("#users");
                 classes.innerHTML = data
             }
            }
        });
});

function editClass(classDetails){
    var className = classDetails[0];
    var userName = classDetails[1];
    var classNameElement = document.getElementById(className+ " ClassName")
    var classNameInputElement = document.createElement("input")
    var user0 = document.getElementById("user 0").innerText;
    classNameInputElement.type = "text"
    classNameInputElement.placeholder = className
    classNameInputElement.id = className+" ClassName"

    classNameElement.replaceWith(classNameInputElement);


    var selectElement = document.createElement("select");
    selectElement.classList.add(userName)
    selectElement.id = className + " UserName"
    var users = document.getElementById('usersList').getElementsByClassName('user');
    console.log(users)
    var option = document.createElement("option");
    option.text = userName;
    selectElement.add(option);
    if (user0 !== userName){
        var option = document.createElement("option");
        option.text = user0
        selectElement.add(option);
    }


    for(var i=0; i<users.length; i++){
        var option = document.createElement("option");
        console.log(option)
        console.log(selectElement.innerText)
        if (selectElement.innerText.includes(users[i].innerText)){
            console.log("stopped")
        }

        else{
            option.text = users[i].innerText;
            selectElement.add(option);
        }
    }

    var oldElement = document.getElementById(className + " UserName");
    oldElement.replaceWith(selectElement);


    var deleteButton = document.getElementById(className + " DeleteButton");
    var exitButton = document.createElement("span");

    exitButton.id = className+" ExitButton";
    exitButton.onclick = function() { exitEdit(classDetails); };
    exitButton.className = "material-symbols-outlined";
    exitButton.innerText = "close";
    deleteButton.replaceWith(exitButton);

    var editButton = document.getElementById(className + " EditButton");
    var doneButton = document.createElement("span")


    doneButton.id = className+" DoneButton";
    doneButton.onclick = function() { submitClassUpdate(classDetails); };
    doneButton.className = "material-symbols-outlined";
    doneButton.innerText = "done";
    editButton.replaceWith(doneButton);
}

function exitEdit(classDetails) {
    var className = classDetails[0]
    var userName = classDetails[1]
    var classNameInput = document.getElementById(className + " ClassName");
    var classNameElement = document.createElement("p")
    classNameElement.id = className + " ClassName"
    classNameElement.innerText = className
    classNameInput.replaceWith(classNameElement)
    var userSelect = document.getElementById(className + " UserName")
    var userNameElement = document.createElement("p")
    userNameElement.id = className + " UserName"
    if (userName === "None"){
        userNameElement.classList = ["noUserWarning"]
        userNameElement.innerText = "No user assigned"
    }
    else{
        userNameElement.innerText = userName
    }
    userSelect.replaceWith(userNameElement)


    var doneButton = document.getElementById(className + " DoneButton")
    var editButton = document.createElement("span")
    editButton.id = className + " EditButton";
    editButton.onclick = function () {
        editClass(classDetails);
    };
    editButton.className = "material-symbols-outlined";
    editButton.textContent = "edit";
    doneButton.replaceWith(editButton);

    var closeButton = document.getElementById(className + " ExitButton")
    var deleteButton = document.createElement("span")
    deleteButton.id = className + " DeleteButton";
    deleteButton.onclick = function () {
        removeClass(classDetails);
    };
    deleteButton.className = "material-symbols-outlined";
    deleteButton.textContent = "delete";
    closeButton.replaceWith(deleteButton);
}


function submitClassUpdate(oldClassDetails){
    var oldClassName = oldClassDetails[0]
    var oldUserName = oldClassDetails[1]
    var newClassName = document.getElementById(oldClassName + " ClassName").value
    var newUserName = document.getElementById(oldClassName + " UserName").value
    if (newClassName !== oldClassName && newClassName !== ""){
        $.ajax({
             type: 'POST',
             url: '/admin',
             data: {
                 trigger:"changeClassName",
                 newClassName: newClassName,
                 oldClassName: oldClassName,
                 userName: oldUserName
             },
            success: function(data) {
                var classes = document.querySelector("#classes");
                classes.innerHTML = data
                }
        });
    };
    if (newUserName !== oldUserName){
        $.ajax({
             type: 'POST',
             url: '/admin',
             data: {
                 trigger:"changeClassUser",
                 newClassName: newClassName,
                 oldClassName: oldClassName,
                 newUserName: newUserName,
                 oldUserName: oldUserName
             },
            success: function(data) {
                 if (data === "That user does not exist."){
                     document.getElementById("notification-text").innerText = "That user does not exist.";
                     notify(3)
                 }
                 else{
                    var classes = document.querySelector("#classes");
                    classes.innerHTML = data
                 }
                }
        });
    }
    exitEdit(oldClassDetails)
}