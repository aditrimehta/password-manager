import React from "react";
import { cn } from "../../utils";

export function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        className
      )}
      {...props}
    />
  );
}
