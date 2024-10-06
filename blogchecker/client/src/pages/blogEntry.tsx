import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useParams, useNavigate } from "react-router-dom";
import { Loader2, Twitter, Megaphone, Mail, Badge } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

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
  is_valid: boolean;
  is_public: boolean;
  last_check_timestamp: string | null;
  created_at: string;
  updated_at: string;
  e2b_run_outputs: E2BRunOutput[];
  blog_code_recipes: BlogCodeRecipe[];
}

interface BlogCodeRecipe {
  id: string;
  title: string;
  description: string;
  language: string;
  success_criteria: string;
  entrypoint: string;
  code_content: string;
}

interface E2BRunOutput {
  id: number;
  title: string;
  published_at: string;
  description: string;
  language: string;
  success_criteria: string;
  entrypoint: string;
  code_content: string;
  stdout: string;
  stderr: string;
  code_interpreter_hostname: string;
  exit_code: number;
  error: boolean;
  created_at: string;
  updated_at: string;
}

import { Check, X } from "lucide-react";

interface StatusIconProps {
  success: boolean;
}

export function StatusIcon({ success = true }: StatusIconProps) {
  return (
    <div className="inline-flex items-center justify-center">
      {success ? (
        <div className="p-2 bg-green-700 rounded-full">
          <Check
            className="w-6 h-6 text-white"
            strokeWidth={3}
            aria-label="Success"
          />
        </div>
      ) : (
        <div className="p-2 bg-red-700 rounded-full">
          <X
            className="w-6 h-6 text-red-100"
            strokeWidth={3}
            aria-label="Failure"
          />
        </div>
      )}
    </div>
  );
}

export function CodeRecipeCards(data: BlogPost) {
  if (!data) {
    return <div>No data available</div>;
  }
  return (
    <div className="flex flex-col gap-4">
      {data.blog_code_recipes.map((recipe, index) =>
        data.e2b_run_outputs[index] ? (
          <CodeRecipeCard
            key={recipe.id}
            recipe={recipe}
            runOutput={data.e2b_run_outputs[index]}
          />
        ) : null,
      )}
    </div>
  );
}
function CodeRecipeCard({
  recipe,
  runOutput,
}: {
  recipe: CodeRecipe;
  runOutput: E2BRunOutput;
}) {
  const [activeTab, setActiveTab] = useState("summary");

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{recipe.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="summary">Summary</TabsTrigger>
            <TabsTrigger value="stderr">stderr</TabsTrigger>
            <TabsTrigger value="stdout">stdout</TabsTrigger>
          </TabsList>
          <TabsContent value="summary" className="space-y-4">
            <div className="grid grid-cols-2 gap-2">
              <div>Language:</div>
              <div>{recipe.language}</div>
              <div>Code Interpreter Hostname:</div>
              <div>{runOutput.code_interpreter_hostname}</div>
              <div>Success:</div>
              <div>
                <StatusIcon success={!runOutput.error} />
              </div>
              <div>Exit Code:</div>
              <div>{runOutput.exit_code}</div>
              <div>Entrypoint:</div>
              <div>{recipe.entrypoint}</div>
            </div>
          </TabsContent>
          <TabsContent value="stderr">
            <pre className="whitespace-pre-wrap text-sm">
              {runOutput.stderr}
            </pre>
          </TabsContent>
          <TabsContent value="stdout">
            <pre className="whitespace-pre-wrap text-sm">
              {runOutput.stdout}
            </pre>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

export default function BlogEntry() {
  console.log("BlogEntry component rendered");
  const [blogPost, setBlogPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const params = useParams();

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

        setBlogPost(blogData);
      } catch (error) {
        console.error("Error fetching blog data:", error);
        setError("Failed to fetch blog data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchBlogData();
  }, [params.id]);

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
      </div>
    );
  }

  if (!blogPost) {
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
              <CardTitle>{blogPost.url}</CardTitle>
              <CardDescription>
                Published: {new Date(blogPost.created_at).toLocaleString()}
              </CardDescription>
            </CardHeader>
          </div>
          <div className="flex justify-end mt-2">
            <div className="mt-2 mr-2">
              <StatusIcon success={blogPost.is_valid} />
            </div>
            <Button
              variant="outline"
              size="lg"
              className="mt-2 mr-2 text-primary hover:text-accent-foreground"
            >
              <Mail className="h-4 w-4 mr-2" />
              JIRA
            </Button>
          </div>
        </div>
        <CodeRecipeCards {...blogPost} />
      </Card>
    </div>
  );
}
