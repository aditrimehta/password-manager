import React from "react";
import { cn } from "../../utils";

export function Button({ children, className, ...props }) {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
