import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import LoginRegister from "./components/LoginRegister";
import Chatbot from "./components/Chatbot";

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check localStorage for token on page load
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) setIsAuthenticated(true);
  }, []);

  return (
    <>
      {!isAuthenticated ? (
        <LoginRegister onLogin={() => setIsAuthenticated(true)} />
      ) : (
        <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
          <Navbar />
          <Chatbot />
        </div>
      )}
    </>
  );
};

export default App;
