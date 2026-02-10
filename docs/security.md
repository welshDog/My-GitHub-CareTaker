# Security Audit Summary

## Token Handling
- Tokens supplied via environment variables; never logged.
- Authorization header only; no persistence by default.
- Enterprise option: encrypted storage can use Redis with encryption at rest.

## Scopes Verification
- Validate via viewer query; operations require repo, security_events, issues, pull_requests.

## Webhooks
- Accept JSON with verification (optional shared secret in future).

## Rate Limits
- Bottleneck limits GraphQL calls; Redis caches heavy results.

## Recommendations
- Rotate tokens; restrict token to least privilege.
