const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");

    if (sender === "user") {

        messageDiv.classList.add("user-message");

        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>You</strong>
                <p>${message}</p>
            </div>
        `;

    } else {

        messageDiv.classList.add("bot-message");

        messageDiv.innerHTML = `
            <div class="avatar">🤖</div>

            <div class="message-content">
                <strong>CampusMate AI</strong>
                <p>${message}</p>
            </div>
        `;
    }

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    // Show user message
    addMessage(message, "user");

    // Clear input
    userInput.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();

        addMessage(data.reply, "bot");

    } catch (error) {

        addMessage(
            "Sorry, I couldn't connect to the server.",
            "bot"
        );
    }
}


// Send button

sendButton.addEventListener("click", sendMessage);


// Enter key

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});
