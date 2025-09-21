import React, { useState, useRef, useEffect } from "react";
import API from "../api";

const Chatbot = ({ token }) => {
  const [messages, setMessages] = useState([
    { text: "Hello! Welcome to Bajaj Vaani, your intelligent finance assistant. How can I help you today?", sender: "bot" },
  ]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
    <div
      style={{
        width: "80%", // slightly wider
        maxWidth: "1000px",
        margin: "100px auto 30px", // below navbar
        display: "flex",
        flexDirection: "column",
        height: "80vh",
        border: "1px solid #ccc",
        borderRadius: "12px",
        overflow: "hidden",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        background: "#f9f9f9",
      }}
    >
      {/* Header */}
      <div
        style={{
          height: "60px",
          background: "#1a5d9f",
          color: "white",
          display: "flex",
          alignItems: "center",
          padding: "0 20px",
          fontWeight: "600",
          fontSize: "18px",
        }}
      >
        Bajaj Vaani
      </div>

      {/* Chat Body */}
      <div
        style={{
          flex: 1,
          padding: "16px",
          display: "flex",
          flexDirection: "column",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
              marginBottom: "10px",
            }}
          >
            <div
              style={{
                maxWidth: "70%",
                padding: "12px 16px",
                borderRadius: "16px",
                background: msg.sender === "user" ? "#cfe2f3" : "#e6f2ff",
                color: "#333",
                boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
                fontSize: "14px",
                lineHeight: "1.4",
                wordBreak: "break-word",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "10px" }}>
            <div
              style={{
                maxWidth: "50%",
                padding: "12px 16px",
                borderRadius: "16px",
                background: "#e6f2ff",
                color: "#333",
                fontStyle: "italic",
                boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              Typing...
            </div>
          </div>
        )}

        <div ref={messagesEndRef}></div>
      </div>

      {/* Input Area */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "12px",
          background: "#f4f4f4",
          borderTop: "1px solid #ddd",
        }}
      >
        <input
          type="text"
          value={query}
          placeholder="Type your question..."
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: 1,
            padding: "10px 16px",
            borderRadius: "20px",
            border: "1px solid #ccc",
            outline: "none",
            fontSize: "14px",
          }}
        />

        <label
          style={{
            padding: "0 12px",
            borderRadius: "50%",
            background: "#1a5d9f",
            color: "white",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          📎
          <input type="file" multiple style={{ display: "none" }} onChange={handleFileChange} />
        </label>

        <button
          onClick={sendMessage}
          style={{
            padding: "0 16px",
            borderRadius: "50%",
            background: "#1a8cff",
            border: "none",
            color: "white",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          ➤
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
