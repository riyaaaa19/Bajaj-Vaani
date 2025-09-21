import React from "react";

const styles = {
  navbar: {
    height: "60px",
    maxWidth: "1000px", // slightly bigger than chat card
    width: "95%", // responsive
    margin: "10px auto", // center horizontally with a small top margin
    background: "#2c3e50",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 20px",
    fontSize: "18px",
    fontWeight: "600",
    borderRadius: "12px",
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
