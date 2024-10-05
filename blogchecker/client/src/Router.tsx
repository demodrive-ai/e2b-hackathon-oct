import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/landing";
import BlogEntry from "./pages/blogEntry.tsx";
import BlogPosts from "./pages/blogs";
export default function Router() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/blogs" element={<BlogPosts />} />
      <Route path="/blogs/:id" element={<BlogEntry />} />
    </Routes>
  );
}
