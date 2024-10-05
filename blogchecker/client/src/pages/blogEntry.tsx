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
  code_content: [];
}

interface E2BRunOutput {
  id: number;
  title: string;
  published_at: string;
  description: string;
  language: string;
  success_criteria: string;
  entrypoint: string;
  code_content: [];
  stdout: string;
  stderr: string;
  exit_code: number;
  error: boolean;
  created_at: string;
  updated_at: string;
}

// const components = {
//   h1: ({ ...props }) => (
//     <h1
//       className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-3xl"
//       {...props}
//     />
//   ),
//   h2: ({ ...props }) => (
//     <h2
//       className="mt-10 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
//       {...props}
//     />
//   ),
//   h3: ({ ...props }) => (
//     <h3
//       className="mt-8 scroll-m-20 text-2xl font-semibold tracking-tight"
//       {...props}
//     />
//   ),
//   p: ({ ...props }) => (
//     <p className="leading-7 [&:not(:first-child)]:mt-6" {...props} />
//   ),
//   a: ({ ...props }) => (
//     <a
//       className="font-medium text-accent underline underline-offset-4"
//       target="_blank"
//       {...props}
//     />
//   ),
//   blockquote: ({ ...props }) => (
//     <blockquote className="mt-6 border-l-2 pl-6 italic" {...props} />
//   ),
//   ul: ({ ...props }) => (
//     <ul className="my-6 ml-6 list-disc [&>li]:mt-2" {...props} />
//   ),
//   table: ({ ...props }) => (
//     <div className="my-6 w-full overflow-y-auto">
//       <table className="w-full" {...props} />
//     </div>
//   ),
//   th: ({ ...props }) => (
//     <th
//       className="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right"
//       {...props}
//     />
//   ),
//   td: ({ ...props }) => (
//     <td
//       className="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right"
//       {...props}
//     />
//   ),
// };

export function CodeRecipeCards(data: BlogPost) {
  if (!data) {
    return <div>No data available</div>;
  }
  console.log("SLEVMA", data);
  return (
    <div className="">
      {data.blog_code_recipes.map((recipe, index) => (
        <CodeRecipeCard
          key={recipe.id}
          recipe={recipe}
          runOutput={data.e2b_run_outputs[index]}
        />
      ))}
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
              <div>Success:</div>
              <div>
                <Badge variant={runOutput.error ? "destructive" : "default"}>
                  {runOutput.error ? "Failed" : "Success"}
                </Badge>
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
