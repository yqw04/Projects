
// Education page
function scrollToSection(sectionId) {
    var section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });
  }

  function toggleDescription() {
    var defaultDescription = document.getElementById('university-year1');
    defaultDescription.style.display = 'block';
    };
  
  function toggleDescription(descriptionId) {
    var descriptions = document.querySelectorAll('.year-modules');
    descriptions.forEach(function(description) {
        description.style.display = 'none'; 
    });
  
    var description = document.getElementById(descriptionId);
    description.style.display = 'block'; 
    }


// Interests page 
var tablinks = document.getElementsByClassName("tab-links")
var tabcontents = document.getElementsByClassName("tab-contents")
function opentab(tabname){
    for(tablelink of tablinks){
        tablelink.classList.remove("active-link");
    }
    for(tabcontent of tabcontents){
        tabcontent.classList.remove("active-tab");
    }
    event.currentTarget.classList.add("active-link");
    document.getElementById(tabname).classList.add("active-tab")
}

function togglePopup(id) {
    var popup = document.getElementById("popup-" + id);
    popup.classList.toggle("active");
}