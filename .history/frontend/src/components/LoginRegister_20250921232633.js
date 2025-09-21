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
        width: "100vw",
        background: "#f5f6f8", // neutral light background
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      }}
    >
      {/* Center Card */}
      <div
        style={{
          width: "450px",
          maxWidth: "90%",
          background: "white",
          borderRadius: "16px",
          boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Header */}
        <div
          style={{
            background: "#1a73e8",
            color: "white",
            padding: "20px",
            fontSize: "1.6rem",
            fontWeight: "600",
            textAlign: "center",
          }}
        >
          Bajaj Vaani
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          style={{
            padding: "30px 25px",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              marginBottom: "25px",
              color: "#1a73e8",
              fontSize: "1.4rem",
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
              padding: "12px 15px",
              marginBottom: "15px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "14px",
              outline: "none",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              padding: "12px 15px",
              marginBottom: "20px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "14px",
              outline: "none",
            }}
          />

          <button
            type="submit"
            style={{
              padding: "12px",
              borderRadius: "8px",
              border: "none",
              background: "#1a73e8",
              color: "white",
              fontWeight: "600",
              fontSize: "14px",
              cursor: "pointer",
              marginBottom: "15px",
              transition: "0.2s",
            }}
            onMouseOver={(e) => (e.currentTarget.style.background = "#1669c1")}
            onMouseOut={(e) => (e.currentTarget.style.background = "#1a73e8")}
          >
            {isLogin ? "Login" : "Register"}
          </button>

          <p
            style={{
              textAlign: "center",
              fontSize: "13px",
              color: "#555",
            }}
          >
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
  );
}
