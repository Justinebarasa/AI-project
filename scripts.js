document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');

    // Example initial message
    appendMessage('bot', 'Hello! How may I help you today?');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent form submission

        // Get user input
        const userInput = document.getElementById('user_input').value;

        // Clear input field
        document.getElementById('user_input').value = '';

        // Append user message to chat box
        appendMessage('user', userInput);

        // Send user input to server via AJAX
        fetch('/enquire', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.response;
            // Append bot response to chat box
            appendMessage('bot', botResponse);
        })
        .catch(error => console.error('Error:', error));
    });

    function appendMessage(sender, message) {
        const messageElem = document.createElement('div');
        messageElem.classList.add('chat-message', sender);
        messageElem.innerText = message;
        chatBox.appendChild(messageElem);
        chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to bottom of chat box
    }
});
