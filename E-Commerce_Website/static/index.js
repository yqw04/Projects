document.addEventListener("DOMContentLoaded", function() {

    // Form handling logic
    const subjectField = document.querySelector("select[name='subject']");
    const otherField = document.getElementById("otherField");

    if (subjectField && otherField) {
        subjectField.addEventListener("change", function() {
            if (subjectField.value === 'other') {
                otherField.style.display = 'block';
            } else {
                otherField.style.display = 'none';
            }
        });

        if (subjectField.value === 'other') {
            otherField.style.display = 'block';
        }
    } else {
        console.log("Form elements not found");
    }

    // Slideshow logic
    let slideIndex = 0;
    showSlides();

    function showSlides() {
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");

        if (slides.length > 0 && dots.length > 0) {
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";  
            }
            slideIndex++;
            if (slideIndex > slides.length) { slideIndex = 1; }
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace(" active", "");
            }
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
            setTimeout(showSlides, 5000); // Change image every 5 seconds
        } else {
            console.log("Slideshow elements not found");
        }
    }
});
