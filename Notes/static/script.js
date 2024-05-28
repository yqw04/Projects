// Used to show popup when user clicks on it
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
