import React, { useState } from "react";
import LoginRegister from "./components/LoginRegister";
import Chatbot from "./components/Chatbot";
import Navbar from "./components/Navbar";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
  };

  if (!token) {
    return <LoginRegister onLogin={(t) => setToken(t)} />;
  }

  return (
    <div>
      <Navbar />
      <div style={{ padding: "20px" }}>
        <button
          onClick={handleLogout}
          style={{
            marginBottom: "10px",
            padding: "8px 12px",
            borderRadius: "6px",
            background: "#e74c3c",
            color: "#fff",
            border: "none",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
        <Chatbot token={token} />
      </div>
    </div>
  );
}
