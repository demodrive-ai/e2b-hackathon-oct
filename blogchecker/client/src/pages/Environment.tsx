import { Button } from "@/components/ui/button";
import React, { useState, useEffect } from "react";
import { toast } from "sonner";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import LeftSidebar from "@/sidebar";
import { Toaster } from "sonner";

export default function Environment() {
  const [envVariables, setEnvVariables] = useState("");

  useEffect(() => {
    const fetchEnvironmentVariables = async () => {
      try {
        const response = await fetch("/api/env/", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          setEnvVariables(data.output);
        } else {
          toast.error("Failed to fetch environment variables");
        }
      } catch (error) {
        console.error("Error fetching environment variables:", error);
        toast.error("An error occurred while fetching environment variables");
      }
    };

    fetchEnvironmentVariables();
  }, []);

  const handleSave = async () => {
    try {
      console.log(envVariables);
      const response = await fetch("/api/env/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: envVariables,
      });

      if (response.ok) {
        toast.success("Environment variables saved successfully");
      } else {
        toast.error("Failed to save environment variables");
      }
    } catch (error) {
      console.error("Error saving environment variables:", error);
      toast.error("An error occurred while saving environment variables");
    }
  };

  return (
    <div className="flex container mx-auto py-10">
      <Toaster />
      <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
        <LeftSidebar />
      </aside>
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Environment Variables</CardTitle>
        </CardHeader>
        <CardContent>
          <textarea
            className="w-full h-64 p-2 border rounded-md mb-4"
            value={envVariables}
            onChange={(e) => setEnvVariables(e.target.value)}
            placeholder="Enter your environment variables here (e.g., KEY=value)"
          />
          <Button
            className="bg-accent text-accent-foreground hover:bg-accent/90"
            onClick={handleSave}
          >
            Save
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
