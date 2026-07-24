const originHosts = (value) =>
  String(value || "")
    .split(",")
    .map((v) => v.trim())
    .map((v) => v.replace(/^https?:\/\//, ""))
    .map((v) => v.replace(/:\d+$/, ""))
    .filter(Boolean);

const wildcardOrigins = ["*.*.*.*", "*.*.*", "*.*"];

const nextConfig = {
  output: "standalone",
  turbopack: {},
  // Next allowedDevOrigins accepts hostnames, not CIDR. These patterns allow any IPv4/LAN origin in dev.
  allowedDevOrigins: [
    "localhost",
    "127.0.0.1",
    ...originHosts(process.env.NEXT_PUBLIC_APP_URL),
    ...originHosts(process.env.NEXT_DEV_ALLOWED_ORIGINS).flatMap((origin) =>
      origin === "*" ? wildcardOrigins : [origin],
    ),
    ...(process.env.NEXT_DEV_ALLOW_ALL_ORIGINS === "true"
      ? wildcardOrigins
      : []),
  ],
  rewrites: async () => [
    {
      source: "/api/:path*",
      destination: `${process.env.BACKEND_API_URL || "http://localhost:8000"}/api/:path*`,
    },
  ],
};

module.exports = nextConfig;
