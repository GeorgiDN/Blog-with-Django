function toggleComments(postId) {
    const commentsDiv = document.getElementById(`comments-${postId}`);

    if (commentsDiv.style.display === "none") {
        commentsDiv.style.display = "block";
    } else {
        commentsDiv.style.display = "none";
    }
}


// Save comment with javascript

// function toggleComments(postId) {
//     const commentsDiv = document.getElementById(`comments-${postId}`);
//
//     // Toggle visibility
//     if (commentsDiv.style.display === "none") {
//         commentsDiv.style.display = "block";
//     } else {
//         commentsDiv.style.display = "none";
//     }
// }
//
// // Add event listener to the 'Add Comment' link
// document.addEventListener("DOMContentLoaded", function () {
//     const commentLinks = document.querySelectorAll('.btn-primary');  // Select all 'Add Comment' links
//
//     commentLinks.forEach(link => {
//         link.addEventListener("click", function (e) {
//             e.preventDefault();  // Prevent the default link behavior
//
//             const form = link.closest("form");
//             const formData = new FormData(form);  // Get form data
//
//             // Create a fetch request to submit the form data
//             fetch(form.action, {
//                 method: 'POST',
//                 body: formData,
//             })
//             .then(response => response.json())  // Assuming a JSON response (adjust if needed)
//             .then(data => {
//                 // Handle successful comment submission
//                 if (data.success) {
//                     // Append the new comment to the list or reload the page to display the new comment
//                     const commentSection = document.getElementById(`comments-${form.dataset.postId}`);
//                     const newComment = `<div class="comment">
//                         <img src="${data.comment_user_profile_img}" class="img-thumbnail rounded-circle" style="width: 40px; height: 40px;" alt="profile-img">
//                         <strong>${data.comment_user_name}</strong>:
//                         <p>${data.comment_text}</p>
//                         <small>${data.comment_date}</small>
//                     </div>`;
//                     commentSection.innerHTML += newComment;
//
//                     // Optionally close the comment section
//                     commentSection.style.display = "none";
//                 }
//             })
//             .catch(error => console.error('Error:', error));
//         });
//     });
// });
