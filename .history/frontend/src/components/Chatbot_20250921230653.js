import React, { useState, useRef, useEffect } from "react";
import API from "../api";

const Chatbot = ({ token }) => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Scroll to bottom whenever messages change
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
        width: "100%",
        maxWidth: "600px",
        margin: "20px auto",
        display: "flex",
        flexDirection: "column",
        height: "80vh",
        border: "1px solid #ddd",
        borderRadius: "12px",
        overflow: "hidden",
        fontFamily: "Arial, sans-serif",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
      }}
    >
      {/* Chat Header */}
      <div
        style={{
          height: "60px",
          background: "#075e54",
          color: "white",
          display: "flex",
          alignItems: "center",
          padding: "0 16px",
          fontWeight: "600",
          fontSize: "16px",
        }}
      >
        Bajaj Vaani
      </div>

      {/* Chat Body */}
      <div
        style={{
          flex: 1,
          padding: "10px",
          background: "#ece5dd",
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
              marginBottom: "8px",
            }}
          >
            <div
              style={{
                maxWidth: "70%",
                padding: "10px 14px",
                borderRadius: "20px",
                background: msg.sender === "user" ? "#dcf8c6" : "white",
                boxShadow: "0 1px 2px rgba(0,0,0,0.2)",
                wordBreak: "break-word",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "8px" }}>
            <div
              style={{
                maxWidth: "50%",
                padding: "10px 14px",
                borderRadius: "20px",
                background: "white",
                boxShadow: "0 1px 2px rgba(0,0,0,0.2)",
                fontStyle: "italic",
              }}
            >
              Typing...
            </div>
          </div>
        )}

        <div ref={messagesEndRef}></div>
      </div>

      {/* File preview */}
      {files.length > 0 && (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "8px",
            padding: "10px",
            background: "#f0f0f0",
          }}
        >
          {files.map((file, idx) => (
            <div
              key={idx}
              style={{
                background: "#fff",
                padding: "6px 10px",
                borderRadius: "12px",
                display: "flex",
                alignItems: "center",
                boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
              }}
            >
              <span>{file.name}</span>
              <button
                style={{
                  marginLeft: "6px",
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  color: "#e74c3c",
                  fontWeight: "bold",
                }}
                onClick={() => removeFile(idx)}
              >
                ❌
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Input area */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "10px",
          background: "#f0f0f0",
        }}
      >
        <input
          type="text"
          value={query}
          placeholder="Type a message"
          onChange={(e) => setQuery(e.target.value)}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "20px",
            border: "1px solid #ccc",
            outline: "none",
          }}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <label
          style={{
            padding: "0 12px",
            borderRadius: "50%",
            background: "#128c7e",
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
            background: "#25d366",
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
