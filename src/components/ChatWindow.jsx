import ProductCard from "./ProductCard";
import "./ChatWindow.css";

export default function ChatWindow({ messages }) {
  console.log("messages", messages)
  return (
    <div className="chat-window">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`chat-message ${msg.sender === "user" ? "user" : "ai"}`}
        >
          {msg.sender === "ai" && msg.data ? (
            <div className="product-list">
              {msg.data.map((p, i) => (
                <ProductCard key={i} product={p} />
              ))}
            </div>
          ) : (msg.sender === "ai" && msg.response ?
            (<div className="message-text">{msg.response}</div>)
            : (<div className="message-text">{msg.text}</div>)
          )}
        </div>
      ))}
    </div>
  );
}


