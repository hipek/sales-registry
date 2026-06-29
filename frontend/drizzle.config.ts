import { defineConfig } from "drizzle-kit"

export default defineConfig({
  dialect: "turso",
  dbCredentials: {
    url: process.env.DATABASE_URL || "file:../data/database.sqlite",
  },
  schema: "./lib/schema.ts",
})
