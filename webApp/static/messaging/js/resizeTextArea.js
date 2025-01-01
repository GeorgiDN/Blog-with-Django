function resizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

const textarea = document.querySelector('textarea');
const charCount = document.getElementById('char-count');

textarea.addEventListener('input', function () {
    charCount.textContent = `${textarea.value.length}/500`;
    resizeTextarea(textarea);
});
