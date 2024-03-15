document.addEventListener("DOMContentLoaded", function() {
    const chatInput = document.getElementById("chat-input");
    const chatSubmit = document.getElementById("chat-submit");
    const chatResponses = document.getElementById("chat-responses");

    chatSubmit.addEventListener("click", function(e) {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (query) {
            fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const responseElement = document.createElement("p");
                responseElement.textContent = data.response;
                chatResponses.appendChild(responseElement);
                chatInput.value = ''; // Clear input after submission
            })
            .catch((error) => {
                console.error('Error during chatbot communication:', error);
                const errorElement = document.createElement("p");
                errorElement.textContent = "Sorry, we couldn't process your request. Please try again later.";
                chatResponses.appendChild(errorElement);
            });
        } else {
            console.error('Chat input is empty.');
            const errorElement = document.createElement("p");
            errorElement.textContent = "Please enter a query before submitting.";
            chatResponses.appendChild(errorElement);
        }
    });
});