import { useState } from "react";

let toastId = 0;

export function useToast() {
  const [toasts, setToasts] = useState([]);

  function showToast(message) {
    const id = ++toastId;
    setToasts([...toasts, { id, message }]);
    setTimeout(() => {
      setToasts((t) => t.filter((toast) => toast.id !== id));
    }, 3000);
  }

  return { toasts, showToast };
}

export function ToastContainer({ toasts }) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className="bg-gray-900 text-white px-4 py-2 rounded-lg shadow"
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
}
