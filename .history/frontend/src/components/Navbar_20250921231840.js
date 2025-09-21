import React from "react";

const styles = {
  container: {
    maxWidth: "900px", // width of your card
    margin: "0 auto", // center horizontally
    display: "flex",
    flexDirection: "column",
    height: "100vh",
  },
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
    borderRadius: "12px 12px 0 0", // rounded corners like a card
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
    <div style={styles.container}>
      <div style={styles.navbar}>
        <div>Bajaj Vaani {username ? `- ${username}` : ""}</div>
        <button style={styles.button} onClick={onLogout}>
          Logout
        </button>
      </div>
      {/* Your Chatbot card will go below this */}
    </div>
  );
};

export default Navbar;
