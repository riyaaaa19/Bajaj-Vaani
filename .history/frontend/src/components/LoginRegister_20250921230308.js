export default function LoginRegister({ onLogin }) {
  // ... existing code ...

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const res = await API.post("/login", { username, password });
        localStorage.setItem("token", res.data.access_token);
        setMessage("✅ Login successful!");
        onLogin(res.data.access_token); // <-- pass token to App.js
      } else {
        await API.post("/register", { username, password });
        setMessage("✅ Registration successful! You can now login.");
        setIsLogin(true);
      }
    } catch (err) {
      setMessage(
        "❌ Error: " + (err.response?.data?.detail || "Something went wrong")
      );
    }
  };

  // ... rest of the component ...
}
