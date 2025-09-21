import React from "react";

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
};

const LoginRegister = ({ onLogin }) => {
  const handleLogin = (e) => {
    e.preventDefault();
    onLogin();
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
          <h2>Login / Register</h2>
          <form onSubmit={handleLogin}>
            <input style={styles.input} type="text" placeholder="Username" required />
            <input style={styles.input} type="password" placeholder="Password" required />
            <button style={styles.button} type="submit">
              Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginRegister;
