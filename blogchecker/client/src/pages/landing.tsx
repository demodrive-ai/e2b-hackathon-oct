import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  PlayCircle,
  CheckCircle,
  Binoculars,
  Code,
  ScrollText,
} from "lucide-react";
import BlurFade from "@/components/magicui/blur-fade";
import { Link as ScrollLink } from "react-scroll";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import WordRotate from "@/components/ui/word-rotate"; // TODO: Implement this component

export default function LandingPage() {
  const navigate = useNavigate();

  const navigateToDashboard = () => {
    navigate("/blogs");
  };

  return (
    <div className="flex flex-col min-h-screen relative">
      {/* Floating Navbar with transparency */}
      <header className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 w-11/12 max-w-6xl">
        <div className="flex items-center justify-between px-6 py-3 bg-secondary/80 backdrop-blur-sm rounded-full shadow-md">
          <div className="flex items-center space-x-2 w-1/3">
            {/* TODO: Replace with actual logo */}
            {/* <div className="w-8 h-8 bg-primary-foreground rounded-full"></div> */}
            <span className="text-2xl font-semibold text-foreground">
              BlogChecker
            </span>
          </div>
          <nav className="hidden md:flex space-x-6 justify-center w-1/3">
            <ScrollLink
              className="text-md font-medium hover:underline cursor-pointer text-primary"
              to="features"
              smooth={true}
              duration={500}
              offset={-100}
            >
              Features
            </ScrollLink>
            <ScrollLink
              className="text-md font-medium hover:underline cursor-pointer text-primary"
              to="demo"
              smooth={true}
              duration={500}
              offset={-200}
            >
              Demo
            </ScrollLink>
          </nav>
          <div className="w-1/3 flex justify-end">
            <Button variant="primary" onClick={navigateToDashboard}>
              Sign In
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-grow pt-24">
        <section className="max-w-4xl mx-auto text-center py-20">
          <BlurFade delay={0.5} inView>
            <h1 className="text-5xl font-semibold mb-6 bg-gradient-to-r from-[#727267] from-8.55% to-[#FFFFF7] to-107% bg-clip-text text-transparent">
              Get more developer love by
            </h1>
            <WordRotate
              words={[
                "building trust",
                "highlighting features",
                "sharing code examples",
              ]}
              className="text-5xl mb-6 bg-gradient-to-r from-[#727267] from-8.55% to-[#FFFFF7] to-107% bg-clip-text text-transparent leading-tight"
            />
          </BlurFade>

          <BlurFade delay={1} inView>
            <Button
              variant="primary"
              className="w-64 h-12 text-lg font-semibold"
            >
              Try it for free
            </Button>
          </BlurFade>
        </section>
        <section id="demo" className="max-w-4xl mx-auto mb-20">
          <BlurFade delay={1.4} duration={0.3} inView>
            <div className="relative aspect-video bg-gray-200 rounded-lg overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center">
                <PlayCircle className="w-16 h-16 text-red-500" />
              </div>
            </div>
          </BlurFade>
        </section>
        <section id="features" className="py-20 bg-primary-background">
          <div className="max-w-6xl mx-auto px-6">
            <h2 className="text-3xl text-secondary-foreground text-center mb-12">
              Convert your product releases into a user magnet
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  title: "Build Trust",
                  description:
                    "Give your users a behind-the-scenes look at what's new and what's improved. Our release notes are designed to build trust, not just list features.",
                  icon: <ScrollText className="h-12 w-12 text-accent" />,
                },
                {
                  title: "Feature Discovery",
                  description:
                    "Are your new features getting the attention they deserve? Our visual assets will make them shine.",
                  icon: <Binoculars className="h-12 w-12 text-accent" />,
                },
                {
                  title: "Engage devs",
                  description:
                    "Tired of throwing code snippets at your dev community and hoping they stick? Our interactive code walkthroughs will make them fall in love with your product.",
                  icon: <Code className="h-12 w-12 text-accent" />,
                },
              ].map((item, i) => (
                <Card
                  key={i}
                  className="transition-all duration-300 hover:shadow-lg border-none"
                >
                  <CardHeader>
                    <div className="flex justify-center mb-4">{item.icon}</div>
                    <CardTitle className="text-xl font-semibold text-center">
                      {item.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-center text-muted-foreground">
                      {item.description}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-primary-background py-12">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-black"></div>
              <span className="text-xl font-semibold">Blogchecker</span>
            </div>
            <nav className="flex flex-wrap justify-center md:justify-end gap-6">
              <Link className="text-sm text-gray-600 hover:underline" href="#">
                Terms of Service
              </Link>
              <Link className="text-sm text-gray-600 hover:underline" href="#">
                Privacy Policy
              </Link>
              <Link className="text-sm text-gray-600 hover:underline" href="#">
                Contact Us
              </Link>
            </nav>
          </div>
        </div>
      </footer>
    </div>
  );
}
