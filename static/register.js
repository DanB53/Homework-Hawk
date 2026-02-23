$(document).on("submit","#register-form", function(event){
    event.preventDefault();
    var user_name = $("input[name='name']").val()
    var password = $("input[name='password']").val()
    var confirm_password = $("input[name='confirmPassword']").val()
    var tempPassword = $("input[name='tempPassword']").val()
    $.ajax({
          type: 'POST',
          url: '/register',
          data: {
              user_name: user_name,
              password: password,
              confirm_password: confirm_password,
              tempPassword: tempPassword
          },
          success: function(data) {
              if (data === "loginRedirect"){
                document.getElementById("notification-text").innerText = "That account is already registered.";
                notify(3)
                  toggleButton()
              }
              else{
                  window.location.href='/home'
              }
          },

          error: function() {
              document.getElementById("notification-text").innerText = "Failed to register.";
              notify(3)

          }
      });
})