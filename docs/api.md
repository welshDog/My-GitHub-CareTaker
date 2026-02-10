# GitHub CareTaker API

## Auth
- GET /api/auth/validate → { ok, viewer }

## Security
- POST /api/security/webhook → Ingest Dependabot-style alert payload and create issue
- GET /api/security/metrics → Aggregated metrics

## Pins
- GET /api/pins/recommendations → Array of top 6 repos

## Duplicates
- GET /api/duplicates/scan → Similar repo pairs with score

## Agents
- POST /api/agents/register → { name, callbackUrl, token? }
- POST /api/agents/webhook → PR event payload queued for agents
