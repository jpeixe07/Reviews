/** @type {import('next').NextConfig} */
const nextConfig = {
  // Cypress/E2E drives behaviour; keep builds unblocked by lint.
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;
