import React from "react";

const Navbar = ({ username, onLogout }) => {
  return (
    <div
      style={{
        height: "60px",
        width: "100%",
        background: "#1a5d9f",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
        fontSize: "18px",
        fontWeight: "600",
        boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 100,
      }}
    >
      <div>Bajaj Vaani</div>
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <span>{username}</span>
        <button
          onClick={onLogout}
          style={{
            padding: "6px 12px",
            borderRadius: "6px",
            border: "none",
            background: "#e74c3c",
            color: "white",
            cursor: "pointer",
            fontWeight: "600",
            fontSize: "14px",
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Navbar;
