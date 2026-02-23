function index(){
    document.location.href = "/"
}
function login(){
    document.location.href = "/login"
}
function contact(){
    document.location.href = "/contact"
}
function profile(){
    document.location.href = "/profile"
}
function classPage(){
    document.location.href = "/class"
}function classesPage(){
    document.location.href = "/classes"
}
function home(){
    document.location.href = "/home"
}
function admin(){
    document.location.href = "/admin"
}


// document.addEventListener('mousemove', (event) => {
//   console.log(`Mouse X: ${event.clientX}, Mouse Y: ${event.clientY}`);
// });

function togglePasswordVisibility(id){
    console.log("toggle");
    var targetIcon = "icon"+id;
    var icon = $("#"+targetIcon);
    var targetBox = "profilePasswordBox"+id;
    console.log(targetBox)
    var box = $("#"+targetBox).attr("type")
    console.log(box)
    if (box == "password"){
        $("#"+targetBox).attr("type","text")
        icon.html("visibility")
    }
    else{
        $("#"+targetBox).attr("type","password")
        icon.html("visibility_off")
    }
}

let notificationText = document.getElementById("notification-text").innerText;
function displayNotification() {
        console.log(notificationText)
        if (notificationText !== "No Notification") {
            if (notificationText === "Couldn't log you in. Check your credentials and try again." && window.location.pathname === "/login"){
                notify(2)
            }
            else if (notificationText === "Successfully changed password." && window.location.pathname === "/login"){
                notify(1)
            }
            else if (notificationText === "Error changing password. Please re-authenticate." && window.location.pathname === "/login"){
                notify(3)
            }
            else if (notificationText === "Failed to scan. Please select students." && "/class" in window.location.pathname){
                notify(2)
            }
            else if (notificationText.includes("Scanning") && window.location.pathname.includes("/class")){
                notify(2)
            }
            else if(notificationText === "Please pick an option on what to scan for!" && window.location.pathname === "/home"){
                notify(2)
            }
            else if(notificationText === "Scanning your manual upload!" && window.location.pathname === "/home"){
                notify(1)
            }
            else if(notificationText === "That account is already registered." && window.location.pathname === "/login"){
                notify(3)
            }
        }


}



window.onload = () => {
    displayNotification()
}

function notify(level){
    if (level == 1){
        $(".notification").css("background-color","rgba(0, 128, 0, 0.319)");
        $("#notification-background").css("background-color","rgba(0, 128, 0, 1)");
    }
    if (level == 2){
        $(".notification").css("background-color","rgba(255, 213, 0, 0.319)");
        $("#notification-background").css("background-color","rgba(255, 213, 0, 1)");
    }
    if (level == 3){
        $(".notification").css("background-color","rgba(255, 49, 49, 0.319)");
        $("#notification-background").css("background-color","rgba(255, 49, 49, 1)");
    }
    $(".notification").css("display", "flex");
    setTimeout(function() {
        if (notificationText === "Couldn't log you in. Check your credentials and try again." && window.location.pathname === "/login"){

            document.getElementById("notification-text").innerText = "No Notification";
            }
        $(".notification").css("display", "none");
    },5000
    );

}

function toggleButton(){
    $("button").attr("disabled", "true");
    $("button").css('background-color', '#1d564c');
    setTimeout(function() {
        $("button").css('background-color', '#5BB3A8');
        $("button").css('transition', '250ms');
        $("button").removeAttr("disabled");
     },5000
     );
}

function make_definition(seed){
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
    var definition = [];
    for (var i = 0; i < charset.length; i++){
        // console.log(charset[i]);
        var pos = charset.charAt(i)
        var key = ""
        var counter = -1
        for (var char = 0; char < charset.length; char++){
            counter = counter + 1
            if (char == i){
                pos = counter
                for (let j = 0; j < 5; j++){
                    pos += seed
                    pos %= charset.length
                    key = key + charset[pos]
                }
                definition.push(key)
                break
            }
        }
    }
    return definition;
}

function encrypt(seed, text){
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
    definition = make_definition(seed);
    var output = "";
    for (var i = 0; i < text.length; i++) {
        var pos = charset.indexOf(text[i]);
        var new_char = definition[pos];
        output = output + new_char
    }
    return output;
}