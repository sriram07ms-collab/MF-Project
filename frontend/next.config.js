/** @type {import('next').NextConfig} */
const repoName = 'MF-Testing-Project'
const isGithubPages = process.env.EXPORT_FOR_GH === 'true'

const nextConfig = {
  reactStrictMode: true,
  output: isGithubPages ? 'export' : 'standalone',
  images: {
    unoptimized: isGithubPages,
  },
  trailingSlash: isGithubPages,
  basePath: isGithubPages ? `/${repoName}` : '',
  assetPrefix: isGithubPages ? `/${repoName}/` : undefined,
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000',
  },
}

module.exports = nextConfig
