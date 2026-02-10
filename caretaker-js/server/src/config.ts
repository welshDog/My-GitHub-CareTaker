export const config = {
  token: process.env.GH_TOKEN || "",
  username: process.env.GH_USERNAME || "welshDog",
  githubApi: process.env.GH_GRAPHQL || "https://api.github.com/graphql",
  githubRest: process.env.GH_API || "https://api.github.com",
  enterprise: process.env.GH_ENTERPRISE || "",
  port: Number(process.env.PORT || 8080),
  redisUrl: process.env.REDIS_URL || "redis://localhost:6379"
}
