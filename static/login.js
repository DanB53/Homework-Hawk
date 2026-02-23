document.getElementById("notification-text").innerText = "No Notification";
$(document).on('submit', '#login-form', function(event) {
    event.preventDefault();
    var details = [];
    $("input").each(function(){
        encrypted_value = encrypt(5486416585555566,$(this).val());
        details.push(encrypted_value);
    });

    $.ajax({
          type: 'POST',
          url: '/login',
          data: JSON.stringify({
              login_details: details
          }),
          contentType: 'application/json;charset=UTF-8',
          success: function(data) {
              console.log(data)
              if (data == "registerRedirect"){
                  window.location.href = '/register'
              }
              else{
                window.location.href = '/home';
              }

          },

          error: function() {
              document.getElementById("notification-text").innerText = "Couldn't log you in. Check your credentials and try again.";
              notify(2)

          }
      });
    
    toggleButton();
});
