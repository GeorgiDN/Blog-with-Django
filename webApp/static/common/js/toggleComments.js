document.addEventListener("DOMContentLoaded", function () {
    const hash = window.location.hash;

    if (hash.startsWith("#comments-")) {
        const postId = hash.replace("#comments-", "");
        const commentsDiv = document.getElementById(`comments-${postId}`);
        if (commentsDiv) {
            commentsDiv.style.display = "block";
        }
    }
});

function toggleComments(postId) {
    const commentsDiv = document.getElementById(`comments-${postId}`);

    if (commentsDiv.style.display === "none") {
        commentsDiv.style.display = "block";
    } else {
        commentsDiv.style.display = "none";
    }
}
