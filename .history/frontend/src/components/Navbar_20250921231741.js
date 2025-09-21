import React from "react";

const styles = {
  navbar: {
    height: "60px",
    background: "#1a5d9f",          // matches chatbot header
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 24px",
    fontSize: "18px",
    fontWeight: "600",
    boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
    borderBottomLeftRadius: "16px",
    borderBottomRightRadius: "16px",
  },
  title: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  button: {
    padding: "6px 14px",
    borderRadius: "8px",
    background: "#ff4d4f",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: "600",
    transition: "background 0.2s",
  },
};

const Navbar = ({ username, onLogout }) => {
  return (
    <div style={styles.navbar}>
      <div style={styles.title}>
        🚀 Bajaj Vaani {username ? `- ${username}` : ""}
      </div>
      <button
        style={styles.button}
        onClick={onLogout}
        onMouseOver={(e) => (e.currentTarget.style.background = "#ff7875")}
        onMouseOut={(e) => (e.currentTarget.style.background = "#ff4d4f")}
      >
        Logout
      </button>
    </div>
  );
};

export default Navbar;
