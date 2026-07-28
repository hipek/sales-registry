const nextJs = require("@next/eslint-plugin-next")

module.exports = [
  {
    files: ["**/*.ts", "**/*.tsx"],
    ignores: [".next/**", "node_modules/**", "dist/**", ".output/**"],
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
