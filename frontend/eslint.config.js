const nextJs = require("@next/eslint-plugin-next")
const parser = require("@typescript-eslint/parser")

module.exports = [
  {
    ignores: [
      ".next/**",
      ".next",
      "node_modules/**",
      "node_modules",
      "dist/**",
      "dist",
      ".output/**",
      ".output",
      "standalone/**",
      "standalone",
      ".pnpm-store/**",
      ".pnpm-store",
    ],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: parser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    plugins: {
      "@next/next": nextJs,
    },
    rules: {
      "@next/next/no-html-link-for-pages": "warn",
      "@next/next/no-img-element": "warn",
      "@next/next/no-page-custom-font": "warn",
    },
  },
]
