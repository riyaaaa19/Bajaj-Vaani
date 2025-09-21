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
};

const Navbar = () => {
  return (
    <div style={styles.navbar}>
      <div>Bajaj Vaani</div>
      <div>User</div>
    </div>
  );
};

export default Navbar;
