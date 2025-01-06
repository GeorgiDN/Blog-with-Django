function resizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

const textarea = document.querySelector('textarea');
const charCount = document.querySelector('.char-count');

textarea.addEventListener('input', function () {
    charCount.textContent = `${textarea.value.length}/1000`;
    resizeTextarea(textarea);
});
