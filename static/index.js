function removeActiveClass() {
    $("#problem").removeClass("active");
    $("#mission").removeClass("active");
    $("#solution").removeClass("active");
    }
  
  function updateCard(description) {
    removeActiveClass();
    $("#desc").html(description);
  }
  
  function problem() {
    updateCard("When students submit work online, it is very hard and inconvenient for the teachers to check whether the students have cheated with either AI (chatGPT etc) or just copy and paste from a source.");
    $("#problem").addClass("active");
  }
  
  function mission() {
    updateCard("We aim to provide teachers with the information and tools that will help them crack down on the problem of students using modern tools such as ChatGPT to do their homework for them.");
    $("#mission").addClass("active");
  }
  
  function solution() {
    updateCard("We offer a simple and easy to use solution for educators by providing a dashboard that educators can use to keep track of whether students have used AI or have just copied and pasted from a source.");
    $("#solution").addClass("active");
  }
  
  window.addEventListener("scroll", (event) => {
    let scroll = this.scrollY;
    console.log(scroll)
    if (scroll >= 231){
      $("#nav").css(
        "z-index", "-100"
      )
    }
    if (scroll < 231){
      $("#nav").css(
        "z-index", "100"
      )
    }
    if (scroll >= 883){
      console.log("swap")
      $("#login-text").css(
        "color", "white"
      )
      $("#contact-text").css(
        "color", "black"
      )
      $(".nav-highlighted").css(
        "background-color", "white",
        "color", "black"
      )

    }
    else{
      $("#login-text").css(
        "color", "black"
      )
      $("#contact-text").css(
        "color", "white"
      )
      $(".nav-highlighted").css(
        "background-color", "#5BB3A8"
      )
    }
});


$(window).on('load', function() {
  if (document.getElementById("firstTime").innerText !== "True"){
    var cookieWrapper = document.getElementById("cookieWrapper")
    cookieWrapper.remove()
  }
  document.getElementById("firstTime").remove()
})

$(document).on("submit","#allowCookiesButton",function(event){
  var cookieWrapper = document.getElementById("cookieWrapper")
  cookieWrapper.remove()
  $.ajax({
       type: 'POST',
       url: '/',
       data: {
         trigger:"allowCookies"
       },
               success: function () {
                    console.log("YES")
                    location.reload()
                 }
  })

})