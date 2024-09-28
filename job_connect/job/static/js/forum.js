document.addEventListener('DOMContentLoaded', function () {
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const fileInput = document.getElementById('file-input');
    const forumBody = document.getElementById('forum-body');
    const onlineUsersList = document.getElementById('online-users');

    // Load messages
    function loadMessages() {
        fetch('/get_messages/')
            .then(response => response.json())
            .then(data => {
                forumBody.innerHTML = '';  // Clear previous messages
                data.messages.forEach(msg => {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message');
                    messageElement.innerHTML = `
                        <strong>${msg.user}</strong> <span class="text-muted">${msg.timestamp}</span><br>
                        <p>${msg.message}</p>
                        ${msg.file ? `<a href="${msg.file}" target="_blank">View File</a>` : ''}
                    `;
                    forumBody.appendChild(messageElement);
                });
                forumBody.scrollTop = forumBody.scrollHeight;  // Scroll to bottom
            });
    }

    // Send message
    messageForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('message', messageInput.value);
        formData.append('file', fileInput.files[0]);
        
        fetch('/send_message/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                messageInput.value = '';  // Clear message input
                fileInput.value = '';  // Clear file input
                loadMessages();  // Reload messages
            }
        });
    });

    // Load online users
    function loadOnlineUsers() {
        fetch('/get_online_users/')
            .then(response => response.json())
            .then(data => {
                onlineUsersList.innerHTML = '';  // Clear previous users
                data.users.forEach(user => {
                    const userElement = document.createElement('li');
                    userElement.textContent = user.username;
                    onlineUsersList.appendChild(userElement);
                });
            });
    }

    // Initial load
    loadMessages();
    loadOnlineUsers();

    // Refresh messages and users every 10 seconds
    setInterval(loadMessages, 10000);
    setInterval(loadOnlineUsers, 10000);
});
