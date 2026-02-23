$(document).on('submit', '#students', function(event) {
    event.preventDefault();
    toggleButton()
    var studentCheckValue = "";
    $(":checkbox").each(function(){
        var isChecked = $(this).is(":checked");
        if (isChecked){
            studentCheckValue = studentCheckValue + $(this).val() + ", ";
        }
    })
    studentCheckValue = studentCheckValue.slice(0, -2);
    className = $("#classname").text()
    var selectedAssignment = $("#assignmentSelect option:selected").text();
    var scanType = $("#scanTypeSelect option:selected").val();
    console.log(studentCheckValue)
    if(studentCheckValue !== ""){
        $(".notification").css("display", "flex");
        $(".notification").css("background-color","rgba(0, 128, 0, 0.319)");
        $("#notification-background").css("background-color","rgba(0, 128, 0, 1)");
        document.getElementById("notification-text").innerText = "Scanning "+studentCheckValue;
        $("#workTooShortMessage").css("display","none")
        $.ajax({
            type: 'POST',
            url: '/class/' + className,
            data: {
                trigger: "student",
                unmarkedStudents: studentCheckValue,
                selectedAssignment: selectedAssignment,
                scanType:scanType
            },

            success: function (data) {
                if (data == "No content") {
                    document.getElementById("notification-text").innerText = "Failed to scan. No content found.";
                    notify(2);
                    $(".notification").css("display", "none");
                } else {
                    var students = document.querySelector("#students");
                    students.innerHTML = data;
                    toggleButton()
                    $(".notification").css("display", "none");
                }
            }
        })
    }
    else{
        document.getElementById("notification-text").innerText = "You must select at least one student to scan.";
        notify(3);
    }

});

$(document).on("change", "#assignment", function(event){
    var selectedAssignment = $("#assignmentSelect option:selected").text();

    className = $("#classname").text()
    $.ajax({
        type:'POST',
        url:'/class/'+className,
        data:{
            trigger:"assignment",
            selectedAssignment: selectedAssignment
        },
        success: function(data) {
            console.log(selectedAssignment)
            var students = document.querySelector("#students");
            if (selectedAssignment != "Select An Assignment"){

                students.innerHTML = data;
            }
            else{
                students.innerHTML = ""
            }
        },
        dataType:"html"
    })
})


$.get('https://app.originality.ai/share/dy6oku3eqx2ap9ht', function(html) {

  // Create div to hold external content
  const $externalContent = $('<div>');

  // Extract portion you want
  const $extractedHtml = $(html).find('#content');
  
  // Insert extracted HTML into div
  $externalContent.html($extractedHtml);

  // Append div to current page
  $('body').append($externalContent);

});
