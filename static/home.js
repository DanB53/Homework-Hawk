$(document).on('submit', '#manual-upload-form', function(event) {
    event.preventDefault();
    var option = ""
    var text = $("textarea").val()
    if ($("#plagiarismCheckbox").is(":checked")){
        option = "pl"
    }
    if ($("#AICheckbox").is(":checked")){
        option = option + "ai"
    }

    if (option === "" || text === "") {
        document.getElementById("notification-text").innerText = "Please pick an option on what to scan for!";
        notify(2)
    }

    else{
        $.ajax({
             type: 'POST',
             url: '/home',
             data: {
                 trigger:"manualUpload",
                 text: text,
                 option: option
             },
            success: function (data) {
                 if (data === "Scan must be min 50 words"){
                     document.getElementById("notification-text").innerText = "Your scan must be a minimum of 50 words.";
                    notify(2)
                 }
                 else {
                     var activities = document.querySelector("#activities");
                     activities.innerHTML = data;
                     toggleButton()
                     document.getElementById("notification-text").innerText = "Scanning your manual upload!";
                     notify(1)
                 }
            }
         })
        ;




    }

})