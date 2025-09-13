import React from "react";
import { cn } from "../../utils";

export function Badge({ children, className, variant = "default" }) {
  const baseStyles =
    "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium";

  const variants = {
    default: "bg-blue-100 text-blue-800",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    danger: "bg-red-100 text-red-800",
    neutral: "bg-gray-100 text-gray-800",
  };

  return (
    <span className={cn(baseStyles, variants[variant], className)}>
      {children}
    </span>
  );
}
