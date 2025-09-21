import React, { useState } from "react";
import API from "../api";

const styles = {
  authContainer: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(120deg, #dfe9f3 0%, #ffffff 100%)",
  },
  authBox: {
    width: "70%",
    height: "70%",
    display: "flex",
    boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
    borderRadius: "12px",
    overflow: "hidden",
  },
  leftColumn: {
    flex: 1,
    background: "linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%)",
    color: "#fff",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },
  rightColumn: {
    flex: 1,
    background: "#fff",
    padding: "40px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },
  input: {
    padding: "12px",
    margin: "10px 0",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "14px",
    width: "100%",
  },
  button: {
    padding: "12px",
    marginTop: "15px",
    border: "none",
    borderRadius: "8px",
    background: "#2c3e50",
    color: "#fff",
    fontSize: "16px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "0.3s",
  },
  toggleText: {
    marginTop: "10px",
    fontSize: "14px",
    cursor: "pointer",
    color: "#2c3e50",
    textDecoration: "underline",
  },
};

const LoginRegister = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const res = await API.post("/auth/login", { username, password });
        localStorage.setItem("token", res.data.access_token);
      } else {
        await API.post("/auth/register", { username, password });
        alert("Registered successfully! Please login.");
        setIsLogin(true);
        return;
      }
      onLogin();
    } catch (err) {
      alert(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div style={styles.authContainer}>
      <div style={styles.authBox}>
        <div style={styles.leftColumn}>
          <h1>Bajaj Vaani</h1>
          <p>
            AI-powered insurance assistant. <br />
            Upload documents, ask queries, and get instant answers.
          </p>
        </div>
        <div style={styles.rightColumn}>
          <h2>{isLogin ? "Login" : "Register"}</h2>
          <form onSubmit={handleAuth}>
            <input
              style={styles.input}
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              style={styles.input}
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button style={styles.button} type="submit">
              {isLogin ? "Login" : "Register"}
            </button>
          </form>
          <div style={styles.toggleText} onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? "New user? Register here" : "Already have an account? Login"}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginRegister;
