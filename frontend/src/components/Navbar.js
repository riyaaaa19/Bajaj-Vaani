import React from "react";

const styles = {
  navbar: {
    height: "70px",           // taller navbar
    width: "100%",            // full width
    position: "fixed",
    top: 0,
    left: 0,
    background: "#2c3e50",
    color: "#fff",
    display: "flex",
    alignItems: "center",     // vertically center content
    justifyContent: "space-between",
    padding: "0 40px",        // enough horizontal padding
    fontSize: "18px",
    fontWeight: "600",
    boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
    zIndex: 1000,
    boxSizing: "border-box",  // include padding in width
  },
  button: {
    padding: "10px 20px",      // bigger padding for proper height
    borderRadius: "6px",
    background: "#e74c3c",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: "600",
    whiteSpace: "nowrap",      // prevent text wrap
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
