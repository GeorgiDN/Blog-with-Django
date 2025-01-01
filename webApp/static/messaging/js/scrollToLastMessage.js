document.addEventListener("DOMContentLoaded", function() {
    const lastMessageElement = document.getElementById("last-message-data");
    const lastMessageId = lastMessageElement ? lastMessageElement.dataset.lastMessageId : null;

    if (lastMessageId) {
        const target = document.getElementById(`message-${lastMessageId}`);
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        }
    }
});

