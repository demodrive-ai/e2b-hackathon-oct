"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Release } from "@/types/release";

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
    accessorKey: "generated_at",
    header: "Generated At",
    cell: ({ row }) => {
      const date = new Date(row.getValue("generated_at"));
      return date.toLocaleString();
    },
  },
];
