import React from "react";
import { cn } from "../../utils";

// Main Card container
export function Card({ children, className }) {
  return (
    <div className={cn("p-4 bg-white rounded-xl shadow-md", className)}>
      {children}
    </div>
  );
}

// CardHeader component
export function CardHeader({ children, className }) {
  return (
    <div className={cn("mb-2", className)}>
      {children}
    </div>
  );
}

// CardContent component
export function CardContent({ children, className }) {
  return (
    <div className={cn("pt-2", className)}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className }) {
    return (
      <h3 className={cn("text-lg font-semibold", className)}>
        {children}
      </h3>
    );
  }
