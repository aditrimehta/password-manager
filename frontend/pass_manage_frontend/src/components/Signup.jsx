import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Mail, Lock, Key } from "lucide-react";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState("signup"); // signup or otp
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Step 1: Send OTP via signup endpoint
  const handleSendOtp = async () => {
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/users/signup/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (res.ok) {
        setStep("otp"); // show OTP input
      } else {
        setError(data.message || "Failed to send OTP");
      }
    } catch (err) {
      setError("Server error. Try again later.");
    }
  };

  // Step 2: Verify OTP
  const handleVerifyOtp = async () => {
    setError("");
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/users/verify-signup-otp/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, otp }),
        }
      );

      const data = await res.json();
      if (res.ok) {
        navigate("/vault"); // redirect to vault after success
      } else {
        setError(data.message || "Invalid OTP");
      }
    } catch (err) {
      setError("Server error. Try again later.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-blue-600 text-center mb-6">
          Create Account
        </h2>

        {step === "signup" && (
          <>
            {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
            <div className="mb-4 relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-500" />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="mb-4 relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-500" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={handleSendOtp}
              className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition mb-4"
            >
              Send OTP
            </button>
            <p className="text-center text-gray-500 text-sm">
              Already have an account?{" "}
              <Link className="text-blue-500 font-medium" to="/">
                Login
              </Link>
            </p>
          </>
        )}

        {step === "otp" && (
          <>
            {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
            <div className="mb-4 relative">
              <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-blue-500" />
              <input
                type="text"
                placeholder="Enter OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={handleVerifyOtp}
              className="w-full bg-blue-500 text-white p-3 rounded-lg font-semibold hover:bg-blue-600 transition mb-4"
            >
              Verify & Signup
            </button>
          </>
        )}
      </div>
    </div>
  );
}
