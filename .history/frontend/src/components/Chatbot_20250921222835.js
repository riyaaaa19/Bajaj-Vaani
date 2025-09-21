import React, { useState } from "react";

const styles = {
  chatContainer: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    padding: "20px",
    background: "#f4f6f9",
  },
  messages: {
    flex: 1,
    overflowY: "auto",
    marginBottom: "10px",
    padding: "10px",
    borderRadius: "10px",
    background: "#ecf0f1",
  },
  messageBubbleUser: {
    alignSelf: "flex-end",
    background: "#2ecc71",
    color: "#fff",
    padding: "10px 15px",
    borderRadius: "18px",
    margin: "5px",
    maxWidth: "70%",
  },
  messageBubbleBot: {
    alignSelf: "flex-start",
    background: "#3498db",
    color: "#fff",
    padding: "10px 15px",
    borderRadius: "18px",
    margin: "5px",
    maxWidth: "70%",
  },
  chatInputArea: {
    display: "flex",
    alignItems: "center",
    padding: "10px",
    borderTop: "1px solid #ccc",
    background: "#fff",
    borderRadius: "10px",
  },
  chatInput: {
    flex: 1,
    padding: "12px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    marginRight: "10px",
    fontSize: "14px",
  },
  button: {
    padding: "10px 15px",
    border: "none",
    borderRadius: "8px",
    background: "#2c3e50",
    color: "#fff",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "0.3s",
  },
  addButton: {
    marginRight: "10px",
    fontSize: "20px",
    cursor: "pointer",
    color: "#2c3e50",
  },
};

const Chatbot = () => {
  const [chatMessages, setChatMessages] = useState([]);
  const [message, setMessage] = useState("");

  const sendMessage = () => {
    if (!message) return;
    setChatMessages([...chatMessages, { text: message, sender: "user" }]);
    setTimeout(() => {
      setChatMessages((prev) => [
        ...prev,
        { text: "Bot reply to: " + message, sender: "bot" },
      ]);
    }, 1000);
    setMessage("");
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.messages}>
        {chatMessages.map((msg, i) => (
          <div
            key={i}
            style={msg.sender === "user" ? styles.messageBubbleUser : styles.messageBubbleBot}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div style={styles.chatInputArea}>
        <span style={styles.addButton}>➕</span>
        <input
          style={styles.chatInput}
          type="text"
          placeholder="Type a message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button style={styles.button} onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
