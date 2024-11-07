$(function() {
    // Initialize the wizard with validation checks
    $("#wizard").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: false, // Disable all steps to ensure sequential navigation
        transitionEffectSpeed: 500,
        labels: {
            finish: "Submit",
            next: "Forward",
            previous: "Backward"
        },
        onStepChanging: function(event, currentIndex, newIndex) {
            // Validate the current step before proceeding
            const currentSection = $("#wizard-p-" + currentIndex);
            const requiredFields = currentSection.find("input[required], select[required], textarea[required]");
            let allFieldsValid = true;

            requiredFields.each(function() {
                if (!this.checkValidity()) {
                    $(this).addClass("is-invalid"); // Add visual feedback for invalid fields
                    allFieldsValid = false;
                } else {
                    $(this).removeClass("is-invalid"); // Remove feedback if field is filled
                }
            });

            // If validation fails, prevent moving to the next step
            return allFieldsValid;
        },
        onFinished: function(event, currentIndex) {
            const form = document.getElementById("wizard");
            if (form.checkValidity()) {
                // Log form data for debugging
                console.log($("#wizard").serializeArray());

                // Submit the form
                form.submit(); // This should trigger a POST request
            } else {
                alert("Please fill out all required fields before submitting.");
            }
        }
    });

    // Custom styling for wizard steps (mark completed steps)
    $("#wizard .steps li a").click(function() {
        $(this).parent().addClass("checked");
        $(this).parent().prevAll().addClass("checked");
        $(this).parent().nextAll().removeClass("checked");
    });

    // Custom select dropdown functionality
    $("html").click(function() {
        $(".select .dropdown").hide();
    });
    $(".select").click(function(event) {
        event.stopPropagation();
    });
    $(".select .select-control").click(function() {
        $(this).parent().next().toggle();
    });
    $(".select .dropdown li").click(function() {
        $(this).parent().toggle();
        var text = $(this).attr("rel");
        $(this).parent().prev().find("div").text(text);
    });
});