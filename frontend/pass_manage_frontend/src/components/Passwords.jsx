import React from "react";

import { PasswordVault } from "./password_vault";
export default function Passwords() {
  return (
    <div className="w-full max-w-lg p-6 rounded shadow-md bg-white border border-gray-200">
      <h2 className="text-2xl font-bold mb-4 text-blue-600">Your Passwords</h2>
      <p className="text-gray-600">This is where all saved passwords will appear.</p>
      <PasswordVault/>
    </div>
  );
}
