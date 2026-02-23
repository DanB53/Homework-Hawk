var minimumFlagPercentageChanged = false



$(document).on('submit', '#passwords', function(event) {
    event.preventDefault();
    var details = [];
    $("input").each(function(){
        details.push($(this).val());
    });
    console.log(details)
    $.ajax({
          type: 'POST',
          url: '/profile',
          data: {
              profilePasswordBox1: details[0],
              profilePasswordBox2: details[1],
              profilePasswordBox3: details[2],
              trigger: "options"
          },
          success: function () {
              document.location.href="/login"

          },
          error: function() {
              document.getElementById("notification-text").innerText = "Error changing password. Please try again.";
              notify(2);
          }
      });
});


$(document).on("change", "#class", function(event){
    var selectedClass = $("#classSelect option:selected").text();

    className = $("#classname").text()
    $.ajax({
        type:'POST',
        url:'/profile',
        data:{
            trigger:"classChange",
            selectedClass: selectedClass
        },
        success: function(data) {
            var automations = document.querySelector("#automations");
            if (selectedClass != "Please select a class"){
                automations.innerHTML = data;
            }
            else{
                automations.innerHTML = ""
            }
        },
        dataType:"html"
    })
});


$(document).on('submit', '#newAutomation', function(event) {
    event.preventDefault()
    var selectedStudent = $("#selectedStudent option:selected").text();
    var selectedOption = $("#selectedOption option:selected").text();
    var selectedClass = $("#classSelect option:selected").text();
    if (selectedStudent === "Add a student"){
        document.getElementById("notification-text").innerText = "Please pick a student to add.";
        notify(2);
        toggleButton()
        return;
    }
    console.log(selectedStudent,selectedOption)
    $.ajax({
          type: 'POST',
          url: '/profile',
          data: {
              trigger: "addAutomation",
              selectedStudent: selectedStudent,
              selectedOption: selectedOption,
              selectedClass: selectedClass
          },
          success: function (data) {
              var automations = document.querySelector("#automations");
              automations.innerHTML = data;
          },
          statusCode:{
              400: function(){
                  document.getElementById("notification-text").innerText = "You can only have one automation per student.";
                  notify(3);
              }
          },
          error: function() {
              document.getElementById("notification-text").innerText = "Error adding automation. Please try again.";
              notify(3);
          }
      });
})

function removeAutomation(value){
    var selectedClass = $("#classSelect option:selected").text();
    $.ajax({
              type: 'POST',
              url: '/profile',
              data: {
                  trigger: "deleteAutomation",
                  first_name: value[0],
                  last_name: value[1],
                  scan_type: value[2],
                  selectedClass: selectedClass
              },
              success: function (data) {
                  var automations = document.querySelector("#automations");
                  automations.innerHTML = data;

              }
          });
}

function sliderChange(){
    var sliderValue = $("#flagPercentageSlider").val()
    var flagPercentageDisplay = document.querySelector("#flagPercentageDisplay");
    flagPercentageDisplay.innerHTML = sliderValue+"%";
    minimumFlagPercentageChanged = true

}


function updateDBMinimumFlagPercentage(){
    var slider = $("#flagPercentageSlider");
    var sliderValue = slider.val();
    console.log(sliderValue);
     $.ajax({
         type: 'POST',
         url: '/profile',
         data: {
             trigger: "changeMinimumFlag",
             newValue:sliderValue
         },
     })
}

$(document).ready(function(){
  var slider = $("#flagPercentageSlider");

  slider.mouseup(function() {
    updateDBMinimumFlagPercentage()
})});


window.onbeforeunload = function(){
    if (minimumFlagPercentageChanged === true){
        updateDBMinimumFlagPercentage()
    }
}