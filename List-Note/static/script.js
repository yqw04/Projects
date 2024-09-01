document.addEventListener('DOMContentLoaded', function () {
    const boxes = document.querySelectorAll('.home-page-box');
    let selectedBox = null;

    // Handle box clicks
    boxes.forEach(box => {
        box.addEventListener('click', function (event) {
            if (selectedBox) {
                selectedBox.classList.remove('selected');
            }
            this.classList.add('selected');
            selectedBox = this;

            // Prevent event from bubbling up to the document click handler
            event.stopPropagation();
        });
    });

    // Handle click anywhere else on the document
    document.addEventListener('click', function () {
        if (selectedBox) {
            selectedBox.classList.remove('selected');
            selectedBox = null;
        }
    });
    
    // Handle Choose button click
    document.getElementById('home-choose-btn').addEventListener('click', function () {
        if (selectedBox) {
            const url = selectedBox.getAttribute('data-url');
            window.location.href = url;
        } else {
            alert('Please select a workspace first.');
        }
    });
});

function togglePopup(id) {
    document.getElementById("popup-" + id).classList.toggle("job_active");
}

// Used to show hints for tags
function showHint() {
    document.getElementById('tags-hint').style.display = 'inline';
}
// Used to show hints for tags
function hideHint() {
    document.getElementById('tags-hint').style.display = 'none';
}