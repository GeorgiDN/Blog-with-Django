window.addEventListener('DOMContentLoaded', (event) => {
    toggleContent();
});

function toggleContent() {
    const sidebarBtn = document.querySelector(".sidebar-button");
    const sidebarList = document.querySelector(".sidebar-list");

    sidebarBtn.addEventListener('click', function () {
        if (sidebarList.style.display === "none") {
            sidebarList.style.display = "block";
            sidebarBtn.textContent = 'Hide';
        } else {
            sidebarList.style.display = "none";
            sidebarBtn.textContent = 'Show';
        }
    });
}
