import React, { useState } from "react";
import API from "../api";

export default function LoginRegister({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const res = await API.post("/login", { username, password });
        localStorage.setItem("token", res.data.access_token);
        setMessage("✅ Login successful!");
        onLogin(res.data.access_token);
      } else {
        await API.post("/register", { username, password });
        setMessage("✅ Registration successful! You can now login.");
        setIsLogin(true);
      }
    } catch (err) {
      setMessage(
        "❌ Error: " + (err.response?.data?.detail || "Something went wrong")
      );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* Left Column */}
      <div
        style={{
          flex: 1,
          background: "linear-gradient(135deg, #4facfe, #00f2fe)",
          color: "white",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          padding: "2rem",
        }}
      >
        <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>🚀 Bajaj Vaani</h1>
        <p style={{ fontSize: "1.2rem", lineHeight: "1.6", textAlign: "center" }}>
          Your intelligent insurance assistant. <br />
          Login or Register to get started.
        </p>
      </div>

      {/* Right Column (Login/Register) */}
      <div
        style={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "#f9f9f9",
        }}
      >
        <form
          onSubmit={handleSubmit}
          style={{
            width: "80%",
            maxWidth: "400px",
            padding: "2rem",
            borderRadius: "12px",
            background: "white",
            boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ textAlign: "center", marginBottom: "1.5rem" }}>
            {isLogin ? "Login" : "Register"}
          </h2>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "1rem",
              borderRadius: "8px",
              border: "1px solid #ddd",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "1rem",
              borderRadius: "8px",
              border: "1px solid #ddd",
            }}
          />

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              background: "#4facfe",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "1rem",
            }}
          >
            {isLogin ? "Login" : "Register"}
          </button>

          <p style={{ marginTop: "1rem", textAlign: "center" }}>
            {isLogin ? "Don't have an account?" : "Already registered?"}{" "}
            <span
              onClick={() => setIsLogin(!isLogin)}
              style={{ color: "#4facfe", cursor: "pointer", fontWeight: "bold" }}
            >
              {isLogin ? "Register" : "Login"}
            </span>
          </p>

          {message && (
            <p
              style={{
                marginTop: "1rem",
                textAlign: "center",
                color: message.startsWith("✅") ? "green" : "red",
              }}
            >
              {message}
            </p>
          )}
        </form>
      </div>
    </div>
  );
}
