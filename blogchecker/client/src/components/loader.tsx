"use client";
import { useEffect, useState } from "react";

export default function Loader() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    import("ldrs").then((mod) => {
      mod.hourglass.register();
      setIsLoaded(true);
    });
  }, []);

  if (!isLoaded) return null;

  return (
    <l-hourglass
      size="40"
      bg-opacity="0.1"
      speed="1.75"
      color="black"
    ></l-hourglass>
  );
}
