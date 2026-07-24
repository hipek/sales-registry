/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  turbopack: {},
  rewrites: async () => [
    {
      source: "/api/:path*",
      destination: `${process.env.BACKEND_API_URL || "http://localhost:8000"}/api/:path*`,
    },
  ],
};

module.exports = nextConfig;
