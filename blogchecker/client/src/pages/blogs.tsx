import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardTitle,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { toast, Toaster } from "sonner";
import { PlusIcon, GitCompare, Sparkles } from "lucide-react";
import Loader from "@/components/loader";
import {
  SuccessToast,
  ErrorToast,
  LoadingToast,
} from "@/components/CustomToast";
import LeftSidebar from "@/sidebar";

export interface BlogPost {
  id: string;
  title: string;
  author: string;
  publish_date: string;
  created_at: string;
  url: string;
}

export default function BlogPosts() {
  const baseUrl = `${window.location.protocol}//${window.location.host}/api`;
  const [blogUrl, setBlogUrl] = useState("");
  const [urlError, setUrlError] = useState("");
  const [isAddingBlog, setIsAddingBlog] = useState(false);
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [analyzedPosts, setAnalyzedPosts] = useState<{
    [key: string]: boolean;
  }>({});

  const fetchBlogPosts = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${baseUrl}/blogs/`, {
        method: "GET",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch blog posts");
      }
      const data = await response.json();
      console.log("Blog posts data:", data);
      setBlogPosts(data);

      // Fetch analysis status for each blog post
      data.forEach((post: BlogPost) => {
        fetchAnalysisStatus(post.id);
      });
    } catch (error) {
      console.error("Error fetching blog posts:", error);
      toast.error(
        <ErrorToast message="Failed to fetch blog posts. Please try again." />,
      );
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBlogPosts();
  }, []);

  const validateAndAddBlog = async () => {
    const blogUrlRegex = /^https?:\/\/.+/;
    if (!blogUrlRegex.test(blogUrl)) {
      setUrlError("Please enter a valid blog post URL");
      return;
    }

    setUrlError("");
    setIsAddingBlog(true);
    const toastId = toast(
      <LoadingToast message="Adding new blog post. This may take a while..." />,
      {
        duration: Infinity,
      },
    );

    try {
      const csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
      const response = await fetch(`${baseUrl}/blogs/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-CSRFToken": csrfToken || "",
        },
        body: JSON.stringify({ url: blogUrl }),
      });

      if (!response.ok) throw new Error("Failed to add blog post");

      const data = await response.json();
      console.log("New blog post added:", data);

      toast.success(
        <SuccessToast message="New blog post added successfully!" />,
        {
          id: toastId,
          duration: 3000,
        },
      );

      setBlogUrl("");
      fetchBlogPosts();
    } catch (error) {
      console.error(error);
      toast.error(
        <ErrorToast message="Failed to add blog post. Please try again." />,
        {
          id: toastId,
          duration: 3000,
        },
      );
    } finally {
      setIsAddingBlog(false);
    }
  };

  const viewResults = (postId: string) => {
    console.log("viewResults called with postId:", postId);
    window.location.href = `/blogs/${postId}`;
  };

  const fetchAnalysisStatus = async (postId: string) => {
    try {
      const response = await fetch(`${baseUrl}/blogs/${postId}/`, {
        method: "GET",
        credentials: "include",
      });
      const data = await response.json();
      if (response.ok && data.analyzed) {
        setAnalyzedPosts((prev) => ({ ...prev, [postId]: true }));
      } else {
        setAnalyzedPosts((prev) => ({ ...prev, [postId]: false }));
      }
    } catch (error) {
      console.error(
        `Error fetching analysis status for blog post ${postId}:`,
        error,
      );
      setAnalyzedPosts((prev) => ({ ...prev, [postId]: false }));
    }
  };

  const analyzeBlogPost = async (postId: string, url: string) => {
    console.log(`Analyzing blog post: ${url}`);

    const toastId = toast(
      <LoadingToast message="Analyzing blog post. This may take a moment..." />,
      { duration: Infinity },
    );

    try {
      const csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
      const response = await fetch(`${baseUrl}/blogs/analyze/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-CSRFToken": csrfToken || "",
        },
        body: JSON.stringify({
          postId: postId,
          url: url,
        }),
      });

      if (response.ok) {
        console.log(`Blog post analyzed: ${url} `);
        toast.success(
          <SuccessToast message="Blog post analyzed successfully!" />,
          { id: toastId, duration: 3000 },
        );
        setAnalyzedPosts((prev) => ({ ...prev, [postId]: true }));
      } else {
        throw new Error("Failed to analyze blog post");
      }
    } catch (error) {
      console.error(`Error analyzing blog post ${url}:`, error);
      toast.error(
        <ErrorToast message="Failed to analyze blog post. Please try again." />,
        { id: toastId, duration: 3000 },
      );
    }
  };

  const formatDate = (dateString: string) => {
    console.log(`Formatting date: ${dateString}`);
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      console.error(`Invalid date format for: ${dateString}`);
      return "Invalid Date";
    }

    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "short",
      day: "numeric",
    };
    const formattedDate = date.toLocaleDateString(undefined, options);
    console.log(`Formatted date for ${dateString}: ${formattedDate}`);
    return formattedDate;
  };

  return (
    <div className="flex container mx-auto py-10">
      <Toaster />
      <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
        <LeftSidebar />
      </aside>
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Blog Posts</CardTitle>
          <CardDescription>Manage and analyze blog posts.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-6">
            <div className="flex space-x-4 mb-4">
              <Input
                type="text"
                placeholder="Enter blog post URL"
                value={blogUrl}
                onChange={(e) => setBlogUrl(e.target.value)}
                className="flex-grow"
                disabled={isAddingBlog}
              />
              <Button
                className="bg-accent text-accent-foreground hover:bg-accent/90"
                onClick={validateAndAddBlog}
                disabled={isAddingBlog}
              >
                <PlusIcon className="w-5 h-5 mr-2" />
                Add New Blog Post
              </Button>
            </div>
            {urlError && <p className="text-red-500 mt-2">{urlError}</p>}
          </div>

          {isLoading ? (
            <div className="flex justify-center items-center h-40">
              <Loader />
            </div>
          ) : (
            <Table className="border-1 border-muted rounded-md">
              <TableHeader className="bg-background text-secondary">
                <TableRow>
                  <TableHead>Url</TableHead>
                  <TableHead>Created At</TableHead>
                  <TableHead>Link</TableHead>
                  <TableHead>Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {blogPosts.map((post) => (
                  <TableRow key={post.id}>
                    <TableCell onClick={() => viewResults(post.id)}>
                      {post.url}
                    </TableCell>
                    <TableCell>
                      {post.created_at ? formatDate(post.created_at) : "N/A"}
                    </TableCell>
                    <TableCell>
                      <a
                        href={post.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <Button variant="outline">View</Button>
                      </a>
                    </TableCell>
                    <TableCell>
                      {analyzedPosts[post.id] ? (
                        <Button
                          variant="outline"
                          onClick={() => viewResults(post.id)}
                        >
                          <GitCompare className="w-4 h-4 mr-2" />
                          Results
                        </Button>
                      ) : (
                        <Button
                          variant="outline"
                          onClick={() => analyzeBlogPost(post.id, post.url)}
                          title="Analyze Blog Post"
                        >
                          <Sparkles className="w-4 h-4" />
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
          {!isLoading && blogPosts.length === 0 && (
            <p className="text-center mt-4">
              No blog posts found. Add a new blog post to get started.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
