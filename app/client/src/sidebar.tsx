import { Link } from "react-router-dom";
import {
  Book,
  Box,
  Settings,
  LogOut,
  MessageSquare,
  MoreVertical,
  User,
  Tag,
  RefreshCw,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useEffect, useState } from "react";
import { toast, Toaster } from "sonner";
import {
  SuccessToast,
  ErrorToast,
  LoadingToast,
} from "@/components/CustomToast";

export default function LeftSidebar() {
  return (
    <div className="fixed inset-y-0 left-0 w-64 bg-background border-r">
      <Toaster />
      <div className="flex h-full flex-col justify-between p-4">
        <div>
          <div className="flex flex-row pl-2">
            <Link to="/">
              <h2 className="mb-6 text-2xl font-bold">BlogChecker</h2>
            </Link>
          </div>
          <nav>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/blogs"
                  className="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700"
                >
                  <Box className="h-6 w-6" />
                  <span className="ml-3">Blogs</span>
                </Link>
              </li>
              <li>
                <Link
                  to="/environment"
                  className="flex items-center rounded-lg p-2 text-base font-normal text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-700"
                >
                  <Settings className="h-6 w-6" />
                  <span className="ml-3">Environment</span>
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  );
}
