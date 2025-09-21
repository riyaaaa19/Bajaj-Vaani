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
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        background: "linear-gradient(to right, #1a73e8, #00c6ff)",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          width: "900px",
          maxWidth: "95%",
          height: "600px",
          background: "white",
          borderRadius: "20px",
          overflow: "hidden",
          boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
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
          <h1 style={{ fontSize: "2.5rem", marginBottom: "1rem" }}>
            🚀 Bajaj Vaani
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              lineHeight: "1.6",
              textAlign: "center",
            }}
          >
            Your intelligent finance assistant. <br />
            Login or Register to get started.
          </p>
        </div>

        {/* Right Column */}
        <div
          style={{
            flex: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            padding: "2rem",
            background: "#f9f9f9",
          }}
        >
          <form
            onSubmit={handleSubmit}
            style={{
              width: "100%",
              maxWidth: "320px",
              background: "white",
              padding: "2rem",
              borderRadius: "12px",
              boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <h2
              style={{
                textAlign: "center",
                marginBottom: "2rem",
                color: "#1a73e8",
              }}
            >
              {isLogin ? "Login" : "Register"}
            </h2>

            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{
                width: "100%",
                padding: "12px 14px",
                marginBottom: "1rem",
                borderRadius: "8px",
                border: "1px solid #ccc",
                outline: "none",
                fontSize: "14px",
              }}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "12px 14px",
                marginBottom: "1rem",
                borderRadius: "8px",
                border: "1px solid #ccc",
                outline: "none",
                fontSize: "14px",
              }}
            />

            <button
              type="submit"
              style={{
                width: "100%",
                padding: "12px",
                borderRadius: "8px",
                border: "none",
                background: "#1a73e8",
                color: "white",
                fontWeight: "600",
                cursor: "pointer",
                fontSize: "14px",
                marginBottom: "1rem",
                transition: "0.2s",
              }}
              onMouseOver={(e) => (e.currentTarget.style.background = "#1669c1")}
              onMouseOut={(e) => (e.currentTarget.style.background = "#1a73e8")}
            >
              {isLogin ? "Login" : "Register"}
            </button>

            <p style={{ textAlign: "center", fontSize: "13px", color: "#555" }}>
              {isLogin ? "Don't have an account?" : "Already registered?"}{" "}
              <span
                onClick={() => setIsLogin(!isLogin)}
                style={{
                  color: "#1a73e8",
                  cursor: "pointer",
                  fontWeight: "600",
                }}
              >
                {isLogin ? "Register" : "Login"}
              </span>
            </p>

            {message && (
              <p
                style={{
                  textAlign: "center",
                  marginTop: "12px",
                  color: message.startsWith("✅") ? "green" : "red",
                  fontSize: "14px",
                }}
              >
                {message}
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
