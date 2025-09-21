import React, { useState } from "react";
import API from "../api";

const styles = {
  container: {
    maxWidth: "600px",
    margin: "20px auto",
    display: "flex",
    flexDirection: "column",
    fontFamily: "Arial, sans-serif",
  },
  chatBox: {
    minHeight: "400px",
    maxHeight: "600px",
    overflowY: "auto",
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "10px",
    marginBottom: "10px",
    background: "#f9f9f9",
  },
  message: {
    marginBottom: "10px",
    padding: "8px 12px",
    borderRadius: "20px",
    maxWidth: "70%",
    wordBreak: "break-word",
  },
  user: {
    background: "#4facfe",
    color: "#fff",
    alignSelf: "flex-end",
  },
  bot: {
    background: "#ecf0f1",
    color: "#000",
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
    borderRadius: "8px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "8px",
    background: "#2ecc71",
    color: "#fff",
    cursor: "pointer",
    fontWeight: "600",
  },
  fileInput: {
    display: "none",
  },
  fileLabel: {
    padding: "8px 12px",
    borderRadius: "8px",
    background: "#f39c12",
    color: "#fff",
    cursor: "pointer",
  },
  filePreview: {
    display: "flex",
    flexWrap: "wrap",
    gap: "8px",
    marginBottom: "10px",
  },
  fileTag: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    padding: "6px 10px",
    borderRadius: "20px",
    background: "#dfe6e9",
    fontSize: "13px",
  },
  removeBtn: {
    background: "transparent",
    border: "none",
    cursor: "pointer",
    fontWeight: "bold",
    color: "#e74c3c",
  },
};

export default function Chatbot({ token }) {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFiles([...files, ...Array.from(e.target.files)]);
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const sendMessage = async () => {
    if (!query.trim() && files.length === 0) return;

    setMessages((prev) => [...prev, { text: query, sender: "user" }]);
    setLoading(true);

    try {
      let res;
      if (files.length > 0) {
        const formData = new FormData();
        files.forEach((f) => formData.append("files", f));
        res = await API.post("/upload", formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        res = await API.post("/chat?query=" + encodeURIComponent(query), null, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }

      setMessages((prev) => [...prev, { text: res.data.answer, sender: "bot" }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { text: "Error: " + (err.response?.data?.detail || err.message), sender: "bot" },
      ]);
    }

    setQuery("");
    setFiles([]);
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
        {loading && <div style={{ ...styles.message, ...styles.bot }}>Thinking...</div>}
      </div>

      {files.length > 0 && (
        <div style={styles.filePreview}>
          {files.map((file, idx) => (
            <div key={idx} style={styles.fileTag}>
              <span>{file.name}</span>
              <button style={styles.removeBtn} onClick={() => removeFile(idx)}>
                ❌
              </button>
            </div>
          ))}
        </div>
      )}

      <div style={styles.inputRow}>
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />

        <label style={styles.fileLabel}>
          +
          <input type="file" multiple onChange={handleFileChange} style={styles.fileInput} />
        </label>

        <button style={styles.button} onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
