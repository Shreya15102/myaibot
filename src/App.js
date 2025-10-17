import { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import InputBox from "./components/InputBox.jsx";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (userMessage) => {
    // Add user message to chat
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);

    // Call backend AI API
    try {
      const response = await fetch("http://127.0.0.1:8000/api/ai-bot/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage }),
      });
      const data = await response.json();

      // Add AI response
      setMessages((prev) => [...prev, { sender: "ai", ...data }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "Oops! Something went wrong." },
      ]);
    }
  };

  return (
    <div className="app-container">
      <header className="header">Mobile Shopping AI Agent</header>
      <ChatWindow messages={messages} />
      <InputBox onSend={sendMessage} />
    </div>
  );
}

