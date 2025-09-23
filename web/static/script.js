document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const chatMessages = document.getElementById("chat-messages");
    const sendButton = document.getElementById("send-button");

    let isConnected = false;
    let isWaitingForResponse = false;

    // Establish WebSocket connection
    const ws = new WebSocket(`ws://${window.location.host}/ws`);

    ws.onopen = (event) => {
        console.log("WebSocket connection established.");
        isConnected = true;
        updateConnectionStatus(true);
        updateButtonState();
    };

    ws.onmessage = (event) => {
        const botMessage = event.data;
        appendMessage(botMessage, "bot");
        isWaitingForResponse = false;
        updateButtonState();
    };

    ws.onerror = (event) => {
        console.error("WebSocket error:", event);
        appendMessage("❌ Sorry, a connection error occurred. Please make sure the API server is running.", "bot");
        isConnected = false;
        isWaitingForResponse = false;
        updateConnectionStatus(false);
        updateButtonState();
    };

    ws.onclose = (event) => {
        console.log("WebSocket connection closed.");
        appendMessage("🔌 Connection closed. Please refresh the page to reconnect.", "bot");
        isConnected = false;
        isWaitingForResponse = false;
        updateConnectionStatus(false);
        updateButtonState();
    };

    chatForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const userMessage = messageInput.value.trim();

        if (userMessage && isConnected && !isWaitingForResponse) {
            appendMessage(userMessage, "user");
            ws.send(userMessage);
            messageInput.value = "";
            isWaitingForResponse = true;
            updateButtonState();

            // Add typing indicator
            appendTypingIndicator();
        }
    });

    function appendMessage(message, sender) {
        // Remove typing indicator if present
        removeTypingIndicator();

        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);

        const messageContent = document.createElement("div");
        messageContent.classList.add("message-content");

        if (sender === "bot") {
            messageContent.innerHTML = `<strong>🤖 Assistant:</strong><p>${formatMessage(message)}</p>`;
        } else {
            messageContent.innerHTML = `<strong>👤 You:</strong><p>${formatMessage(message)}</p>`;
        }

        messageElement.appendChild(messageContent);
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendTypingIndicator() {
        const typingElement = document.createElement("div");
        typingElement.classList.add("message", "bot-message", "typing-indicator");
        typingElement.innerHTML = '<div class="message-content"><strong>🤖 Assistant:</strong><p>Thinking...</p></div>';
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.querySelector(".typing-indicator");
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function formatMessage(message) {
        // Basic formatting - convert line breaks to <br>
        return message.replace(/\n/g, '<br>');
    }

    function updateButtonState() {
        if (isWaitingForResponse) {
            sendButton.disabled = true;
            sendButton.innerHTML = "...";
        } else if (!isConnected) {
            sendButton.disabled = true;
            sendButton.innerHTML = "Disconnected";
        } else {
            sendButton.disabled = false;
            sendButton.innerHTML = "<span>Send</span>";
        }
    }

    function updateConnectionStatus(connected) {
        // Could add a visual connection indicator here
        if (connected) {
            console.log("✅ Connected to chatbot");
        } else {
            console.log("❌ Disconnected from chatbot");
        }
    }

    // Focus on input when page loads
    messageInput.focus();

    // Initialize button state
    updateButtonState();
}); 