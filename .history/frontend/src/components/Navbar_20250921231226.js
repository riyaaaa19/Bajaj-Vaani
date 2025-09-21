import React from "react";

const styles = {
  navbar: {
    height: "60px",
    background: "#2c3e50",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 20px",
    fontSize: "18px",
    fontWeight: "600",
    boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
  },
  button: {
    padding: "6px 12px",
    borderRadius: "6px",
    background: "#e74c3c",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    fontSize: "14px",
  },
};

const Navbar = ({ username, onLogout }) => {
  return (
    <div style={styles.navbar}>
      <div>Bajaj Vaani {username ? `- ${username}` : ""}</div>
      <button style={styles.button} onClick={onLogout}>
        Logout
      </button>
    </div>
  );
};

export default Navbar;
