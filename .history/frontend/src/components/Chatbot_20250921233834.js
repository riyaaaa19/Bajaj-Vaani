import React, { useState, useRef, useEffect } from "react";
import API from "../api";

const Chatbot = ({ token }) => {
  const [messages, setMessages] = useState([
    {
      text: "Hello! Welcome to Bajaj Vaani, your intelligent finance assistant. How can I help you today?",
      sender: "bot",
    },
  ]);
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fileFlag, setFileFlag] = useState(""); // temporary document flag

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, fileFlag]);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);

    // Show temporary flag above chat
    if (selectedFiles.length > 0) {
      setFileFlag(`📎 Document "${selectedFiles[0].name}" attached.`);
    }
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const sendMessage = async () => {
    if (!query.trim() && files.length === 0) return;

    // Add user message if typing text
    if (query.trim()) {
      setMessages((prev) => [...prev, { text: query, sender: "user" }]);
    }

    setLoading(true);
    setQuery(""); // clear input immediately
    setFileFlag(""); // clear flag after send, it will be shown above chat instead

    try {
      let res;
      if (files.length > 0) {
        const formData = new FormData();
        files.forEach((f) => formData.append("files", f));
        res = await API.post("/upload", formData, {
          headers: { Authorization: `Bearer ${token}` },
        });

        // Show chat message that document was sent
        setMessages((prev) => [
          ...prev,
          {
            text: `📎 You sent document(s): ${files.map((f) => f.name).join(", ")}`,
            sender: "user",
            isDocument: true,
          },
        ]);
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

    setFiles([]);
    setLoading(false);
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "800px",
        margin: "20px auto",
        display: "flex",
        flexDirection: "column",
        height: "85vh",
        border: "1px solid #ccc",
        borderRadius: "12px",
        overflow: "hidden",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
        background: "#f9f9f9",
      }}
    >

      {/* Temporary File Flag */}
      {fileFlag && (
        <div
          style={{
            padding: "8px 16px",
            background: "#e6f2ff",
            color: "#333",
            fontStyle: "italic",
            borderBottom: "1px solid #ddd",
          }}
        >
          {fileFlag}
        </div>
      )}

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
                fontStyle: msg.isDocument ? "italic" : "normal",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              marginBottom: "10px",
            }}
          >
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

      {/* File Preview */}
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
