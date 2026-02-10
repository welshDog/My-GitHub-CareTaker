# Deployment Guide

## Prerequisites
- Docker + Docker Compose
- GitHub token with repo, security_events, issues, pull_requests

## Steps
1. Set environment variables GH_TOKEN and GH_USERNAME
2. Run: docker-compose up --build
3. Open web at http://localhost:5173

## GitHub Enterprise
Set GH_GRAPHQL and GH_API to your enterprise endpoints before starting.
