document.getElementById("send-btn").addEventListener("click", async function () {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const message = userInput.value.trim();
  const API_BASE_URL = "http://localhost:8000"; // Make sure this matches your backend URL

  if (message !== "") {
    // Add user message
    const userMessage = document.createElement("div");
    userMessage.classList.add("chat-message", "user-message");
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);
    userMessage.scrollIntoView({ behavior: "smooth" });

    // Clear input
    userInput.value = "";

    // Add loading message
    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("chat-message", "bot-message");
    loadingMessage.innerHTML = `<strong>Lumi is thinking... 💭</strong>`;
    chatBox.appendChild(loadingMessage);
    loadingMessage.scrollIntoView({ behavior: "smooth" });

    try {
      // Request to backend
      const response = await fetch(`${API_BASE_URL}/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          wallet_address: "test_user", // Replace with actual user ID or wallet
          user_message: message
        })
      });

      const data = await response.json();

      // Remove loading
      chatBox.removeChild(loadingMessage);

      // Add bot response with line breaks
      const botMessage = document.createElement("div");
      botMessage.classList.add("chat-message", "bot-message");
      const formattedResponse = data.bot_response.replace(/\n/g, "<br>");
      botMessage.innerHTML = formattedResponse;
      chatBox.appendChild(botMessage);
      botMessage.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      // Handle errors
      chatBox.removeChild(loadingMessage);
      const errorMessage = document.createElement("div");
      errorMessage.classList.add("chat-message", "bot-message");
      errorMessage.textContent = "⚠️ Lumi couldn't respond. Please try again later!";
      chatBox.appendChild(errorMessage);
    }
  }
});
