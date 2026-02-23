$(document).on('submit', '#contact-content', function(event) {
    event.preventDefault();
    toggleButton()
    var email = $("#email").val()
    var message = $("#message").val()
    if (email == ""){
        document.getElementById("notification-text").innerText = "You must add an email.";
        notify(2);
    }
    else if (message == ""){
        document.getElementById("notification-text").innerText = "You must add a message.";
        notify(2);
    }
    else{
        $.ajax({
            type: 'POST',
            url: '/contact',
            data: {
                trigger: "newContact",
                email:email,
                message:message
            },

            success: function (data) {
                if (data == "success") {
                    document.getElementById("notification-text").innerText = "Your message has been sent.";
                    notify(1);
                } else {
                    document.getElementById("notification-text").innerText = "There was an error sending your message";
                    notify(3);
                    toggleButton()
                }
            }
        })
    }

})