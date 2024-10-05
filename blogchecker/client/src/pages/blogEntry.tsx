import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useParams, useNavigate } from "react-router-dom";
import removeMarkdown from "remove-markdown";
import {
  Loader2,
  CopyIcon,
  CheckIcon,
  Twitter,
  Megaphone,
  Mail,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import LeftSidebar from "@/sidebar";

interface BlogPost {
  id: string;
  url: string;
  title: string;
  content: string;
  created_at: string;
}

interface AnalyzedBlogPost {
  id: string;
  improved_content: string;
  summary: string;
  created_at: string;
}

const components = {
  h1: ({ ...props }) => (
    <h1
      className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-3xl"
      {...props}
    />
  ),
  h2: ({ ...props }) => (
    <h2
      className="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
      {...props}
    />
  ),
  h3: ({ ...props }) => (
    <h3
      className="mt-8 scroll-m-20 text-2xl font-semibold tracking-tight"
      {...props}
    />
  ),
  p: ({ ...props }) => (
    <p className="leading-7 [&:not(:first-child)]:mt-6" {...props} />
  ),
  a: ({ ...props }) => (
    <a
      className="font-medium text-accent underline underline-offset-4"
      target="_blank"
      {...props}
    />
  ),
  blockquote: ({ ...props }) => (
    <blockquote className="mt-6 border-l-2 pl-6 italic" {...props} />
  ),
  ul: ({ ...props }) => (
    <ul className="my-6 ml-6 list-disc [&>li]:mt-2" {...props} />
  ),
  table: ({ ...props }) => (
    <div className="my-6 w-full overflow-y-auto">
      <table className="w-full" {...props} />
    </div>
  ),
  th: ({ ...props }) => (
    <th
      className="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right"
      {...props}
    />
  ),
  td: ({ ...props }) => (
    <td
      className="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right"
      {...props}
    />
  ),
};

export default function BlogEntry() {
  console.log("BlogEntry component rendered");
  const [blogPost, setBlogPost] = useState<BlogPost | null>(null);
  const [analyzedBlogPost, setAnalyzedBlogPost] =
    useState<AnalyzedBlogPost | null>(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const params = useParams();
  const navigate = useNavigate();

  console.log("BlogEntry rendered, params:", params);

  useEffect(() => {
    const fetchBlogData = async () => {
      setLoading(true);
      setError(null);
      console.log("Fetching blog data for id:", params.id);
      try {
        const baseUrl = `${window.location.protocol}//${window.location.host}/api`;
        console.log("Base URL:", baseUrl);

        const blogResponse = await fetch(`${baseUrl}/blogs/${params.id}/`, {
          method: "GET",
          credentials: "include",
        });
        console.log("Blog response status:", blogResponse.status);

        if (!blogResponse.ok) {
          throw new Error("Failed to fetch blog data");
        }

        const blogData = await blogResponse.json();
        console.log("Blog data:", blogData);

        const analyzedBlogData = blogData.analyzed_blog_post;
        console.log("Analyzed blog data:", analyzedBlogData);

        setBlogPost(blogData);
        setAnalyzedBlogPost(analyzedBlogData);
      } catch (error) {
        console.error("Error fetching blog data:", error);
        setError("Failed to fetch blog data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchBlogData();
  }, [params.id]);

  const copyToClipboard = () => {
    if (analyzedBlogPost) {
      navigator.clipboard.writeText(analyzedBlogPost.improved_content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const shareOnTwitter = () => {
    if (analyzedBlogPost && blogPost) {
      const tweetText = encodeURIComponent(
        removeMarkdown(
          `Check out this blog post: ${blogPost.title}\n${analyzedBlogPost.summary.slice(0, 140)}...`,
        ),
      );
      const tweetUrl = `https://twitter.com/intent/tweet?text=${tweetText}&url=${encodeURIComponent(blogPost.url)}`;
      window.open(tweetUrl, "_blank");
    }
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  console.log(
    "Current state - blogPost:",
    blogPost,
    "analyzedBlogPost:",
    analyzedBlogPost,
    "loading:",
    loading,
    "error:",
    error,
  );

  if (loading) {
    return (
      <div className="flex container mx-auto py-10">
        <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
          <LeftSidebar />
        </aside>
        <div className="flex-grow flex items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex container mx-auto py-10">
        <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
          <LeftSidebar />
        </aside>
        <Card className="flex-grow">
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-500">{error}</p>
            <Button onClick={handleGoBack} className="mt-4">
              Go Back
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!blogPost || !analyzedBlogPost) {
    console.log("No blog post or analyzed blog post data");
    return (
      <div className="flex container mx-auto py-10">
        <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
          <LeftSidebar />
        </aside>
        <Card className="flex-grow">
          <CardContent>
            <p>No blog data available.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex container mx-auto py-10">
      <aside className="w-64 flex-shrink-0 h-full overflow-y-auto">
        <LeftSidebar />
      </aside>
      <Card className="flex-grow">
        <div className="flex justify-between">
          <div className="flex justify-start">
            <CardHeader>
              <CardTitle>{blogPost.title}</CardTitle>
              <CardDescription>
                Published: {new Date(blogPost.created_at).toLocaleString()}
              </CardDescription>
            </CardHeader>
          </div>
          <div className="flex justify-end mt-2">
            <Button
              variant="outline"
              size="lg"
              className="mt-2 mr-2 text-accent hover:text-accent-foreground"
              onClick={shareOnTwitter}
            >
              <Twitter className="h-4 w-4 mr-2" />
              <span>Tweet</span>
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="mt-2 mr-2 text-accent hover:text-accent-foreground"
            >
              <Mail className="h-4 w-4 mr-2" />
              Email
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="mt-2 mr-2 text-accent hover:text-accent-foreground"
              onClick={() => window.open(blogPost.url, "_blank")}
            >
              <Megaphone className="h-4 w-4 mr-2" />
              View Original
            </Button>
          </div>
        </div>
        <CardContent className="pt-5">
          <div className="flex space-x-4 h-[calc(100vh-300px)]">
            <div className="flex-1 flex flex-col">
              <h2 className="text-xl font-semibold mb-2 text-center">
                Original Content
              </h2>
              <Card className="flex-grow overflow-hidden">
                <ScrollArea className="h-full p-4">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeRaw]}
                    components={components}
                  >
                    {blogPost.content}
                  </ReactMarkdown>
                </ScrollArea>
              </Card>
            </div>
            <div className="flex-1 flex flex-col">
              <h2 className="text-xl font-semibold mb-2 text-center">
                Improved Content
              </h2>
              <Card className="flex-grow overflow-hidden relative border border-primary">
                <Button
                  variant="outline"
                  size="icon"
                  className="absolute top-2 right-2 z-10"
                  onClick={copyToClipboard}
                >
                  {copied ? (
                    <CheckIcon className="h-4 w-4" />
                  ) : (
                    <CopyIcon className="h-4 w-4" />
                  )}
                </Button>
                <ScrollArea className="h-full p-4">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeRaw]}
                    components={components}
                  >
                    {analyzedBlogPost.improved_content}
                  </ReactMarkdown>
                </ScrollArea>
              </Card>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
