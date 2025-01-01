function updateFileName(input) {
    const fileNameSpan = document.getElementById("fileName");
    if (input.files && input.files[0]) {
        fileNameSpan.textContent = input.files[0].name;
    } else {
        fileNameSpan.textContent = '';
    }
}
