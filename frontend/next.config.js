/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,

  // If you use <Image /> with remote images, configure allowed hosts here.
  images: {
    remotePatterns: [
      // Example placeholders. Add the domains you actually use.
      // { protocol: "https", hostname: "images.unsplash.com" },
      // { protocol: "https", hostname: "cdn.yourdomain.com" },
    ],
  },

  // Helpful for deployments where you want builds to succeed even if lint isn't clean yet.
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Same idea for TypeScript during early deployment; remove once stable.
  typescript: {
    ignoreBuildErrors: true,
  },

  // Proxy /api/* calls to your backend (FastAPI on Railway)
  // Requires NEXT_PUBLIC_API_BASE_URL in Vercel env vars, e.g.
  // https://your-backend.up.railway.app
  async rewrites() {
    const base = process.env.NEXT_PUBLIC_API_BASE_URL;

    // If not set, do not add rewrites (prevents invalid destination and build issues)
    if (!base) return [];

    return [
      {
        source: "/api/:path*",
        destination: `${base}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
