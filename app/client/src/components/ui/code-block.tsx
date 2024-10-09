import React from "react";
import { cn } from "@/lib/utils";

interface CodeBlockProps extends React.HTMLAttributes<HTMLPreElement> {
  content: string;
}

export const CodeBlock = React.forwardRef<HTMLPreElement, CodeBlockProps>(
  ({ content, className, ...props }, ref) => {
    return (
      <pre
        ref={ref}
        className={cn(
          "rounded-md bg-muted p-4 overflow-x-auto",
          "text-sm font-mono text-muted-foreground",
          className,
        )}
        {...props}
      >
        <code>{content}</code>
      </pre>
    );
  },
);

CodeBlock.displayName = "CodeBlock";
