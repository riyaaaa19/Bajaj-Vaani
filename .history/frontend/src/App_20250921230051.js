import React, { useState } from "react";
import Chatbot from "./src/Chatbot";

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
      } else {
        setError(data.detail || "Login failed");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
  };

  if (!token) {
    // Login Page
    return (
      <div style={{ width: "400px", margin: "50px auto", padding: "20px", background: "#f4f6f8", borderRadius: "10px" }}>
        <h2>Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px", borderRadius: "6px" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px", borderRadius: "6px" }}
        />
        <button onClick={handleLogin} style={{ width: "100%", padding: "10px", background: "#2ecc71", color: "#fff", borderRadius: "6px", fontWeight: "600" }}>
          Login
        </button>
        {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      </div>
    );
  }

  // If logged in, show Chatbot
  return (
    <div>
      <button onClick={handleLogout} style={{ position: "absolute", right: "20px", top: "20px", padding: "8px 12px", background: "#e74c3c", color: "#fff", border: "none", borderRadius: "6px", cursor: "pointer" }}>
        Logout
      </button>
      <Chatbot />
    </div>
  );
};

export default App;
