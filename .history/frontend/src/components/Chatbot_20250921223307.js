import React, { useState } from "react";
import axios from "axios";

const styles = {
  container: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    background: "#f4f6f8",
    padding: "20px",
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    marginBottom: "10px",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    background: "#fff",
  },
  message: {
    marginBottom: "10px",
    padding: "8px 12px",
    borderRadius: "6px",
    maxWidth: "70%",
  },
  user: {
    background: "#3498db",
    color: "#fff",
    alignSelf: "flex-end",
  },
  bot: {
    background: "#ecf0f1",
    alignSelf: "flex-start",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    fontSize: "14px",
  },
  fileInput: {
    border: "1px solid #ccc",
    borderRadius: "6px",
    padding: "6px",
    background: "#fff",
  },
  button: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "6px",
    background: "#2ecc71",
    color: "#fff",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
  },
};

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState(null);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("token");

  const sendMessage = async () => {
    if (!query.trim() && !files) return;

    // show user message immediately
    setMessages((prev) => [...prev, { text: query, sender: "user" }]);

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("query", query);
      if (files) {
        for (let i = 0; i < files.length; i++) {
          formData.append("files", files[i]);
        }
      }

      const res = await axios.post("/chat", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setMessages((prev) => [...prev, { text: res.data.answer, sender: "bot" }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { text: "Error: " + (err.response?.data?.detail || err.message), sender: "bot" },
      ]);
    }

    setQuery("");
    setFiles(null);
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatBox}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              ...styles.message,
              ...(msg.sender === "user" ? styles.user : styles.bot),
            }}
          >
            {msg.text}
          </div>
        ))}
        {loading && <div style={styles.bot}>Thinking...</div>}
      </div>

      <div style={styles.inputRow}>
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <input
          type="file"
          multiple
          onChange={(e) => setFiles(e.target.files)}
          style={styles.fileInput}
        />
        <button style={styles.button} onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
