import { ColumnDef } from "@tanstack/react-table";
import { Release } from "@/pages/releases";
import React from "react";

export const columns: ColumnDef<Release>[] = [
  {
    accessorKey: "repo_name",
    header: "Repository",
  },
  {
    accessorKey: "release_name",
    header: "Release",
  },
  {
    accessorKey: "published_at",
    header: "Published At",
  },
  {
    accessorKey: "release_url",
    header: "URL",
    cell: ({ row }) =>
      React.createElement(
        "a",
        {
          href: row.original.release_url,
          target: "_blank",
          rel: "noopener noreferrer",
          className: "text-blue-500 hover:underline",
        },
        "View",
      ),
  },
];
