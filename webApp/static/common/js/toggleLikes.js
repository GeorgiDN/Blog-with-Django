function toggleLikes(postId) {
    const likesDiv = document.getElementById(`likes-${postId}`);

    if (likesDiv.style.display === "none") {
        likesDiv.style.display = "block";
    } else {
        likesDiv.style.display = "none";
    }
}
