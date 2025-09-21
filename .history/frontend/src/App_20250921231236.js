import React, { useState } from "react";
import LoginRegister from "./components/LoginRegister";
import Chatbot from "./components/Chatbot";
import Navbar from "./components/Navbar";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [username, setUsername] = useState(localStorage.getItem("username") || "");

  const handleLogin = (t, u) => {
    setToken(t);
    setUsername(u);
    localStorage.setItem("token", t);
    localStorage.setItem("username", u);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken("");
    setUsername("");
  };

  if (!token) {
    return <LoginRegister onLogin={handleLogin} />;
  }

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <Navbar username={username} onLogout={handleLogout} />
      <div style={{ flex: 1 }}>
        <Chatbot token={token} />
      </div>
    </div>
  );
}
