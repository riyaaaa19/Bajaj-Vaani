import React, { useState } from "react";
import axios from "axios";

const styles = {
  container: {
    width: "500px",
    margin: "50px auto",
    display: "flex",
    flexDirection: "column",
    background: "#f4f6f8",
    borderRadius: "10px",
    padding: "20px",
    boxShadow: "0px 4px 15px rgba(0,0,0,0.1)",
    height: "700px",
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    background: "#fff",
    marginBottom: "10px",
  },
  message: {
    marginBottom: "10px",
    padding: "10px 14px",
    borderRadius: "20px",
    maxWidth: "70%",
    wordBreak: "break-word",
  },
  user: {
    background: "#3498db",
    color: "#fff",
    alignSelf: "flex-end",
  },
  bot: {
    background: "#ecf0f1",
    color: "#2c3e50",
    alignSelf: "flex-start",
  },
  inputRow: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
  },
  input: {
    flex: 1,
    padding: "12px",
    borderRadius: "20px",
    border: "1px solid #ccc",
    fontSize: "14px",
  },
  fileInput: {
    display: "none",
  },
  uploadBtn: {
    padding: "8px 14px",
    border: "none",
    borderRadius: "6px",
    background: "#f39c12",
    color: "#fff",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
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

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("token"); // Ensure token is set

  const handleFileChange = (e) => {
    setFiles([...files, ...Array.from(e.target.files)]);
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const sendMessage = async () => {
    if (!query.trim() && files.length === 0) return;

    // Show user message
    if (query.trim()) {
      setMessages((prev) => [...prev, { text: query, sender: "user" }]);
    }
    setLoading(true);

    try {
      let res;
      if (files.length > 0 && !query.trim()) {
        // Only files → /upload
        const formData = new FormData();
        files.forEach((file) => formData.append("files", file));

        res = await axios.post("http://127.0.0.1:8000/upload", formData, {
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" },
        });
      } else {
        // Text or text + files → /chat
        const formData = new FormData();
        formData.append("query", query);
        files.forEach((file) => formData.append("files", file));

        res = await axios.post("http://127.0.0.1:8000/chat", formData, {
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" },
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

        <label style={styles.uploadBtn}>
          +
          <input type="file" multiple onChange={handleFileChange} style={styles.fileInput} />
        </label>

        <button style={styles.button} onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
