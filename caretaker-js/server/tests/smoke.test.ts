import request from 'supertest'
import { app } from '../src/index'
import Redis from 'ioredis-mock'
import { describe, expect, test, beforeAll, afterAll, jest } from '@jest/globals'

// Mock dependencies
jest.mock('ioredis', () => require('ioredis-mock'))
jest.mock('../src/config', () => ({
  config: {
    port: 0,
    redisUrl: 'redis://localhost:6379',
    token: 'ghp_test',
    username: 'tester',
    githubRest: 'https://api.github.com'
  }
}))
// Mock GitHub client
jest.mock('../src/github', () => {
  return {
    GitHub: jest.fn().mockImplementation(() => ({
      viewer: jest.fn().mockImplementation(() => Promise.resolve({ viewer: { login: 'tester' } })),
      reposByUser: jest.fn().mockImplementation(() => Promise.resolve([
        { name: 'repo1', description: 'test repo', stargazerCount: 10, forkCount: 2, updatedAt: '2023-01-01', pushedAt: '2023-01-01' },
        { name: 'repo2', description: 'test repo', stargazerCount: 5, forkCount: 0, updatedAt: '2023-01-01', pushedAt: '2023-01-01' }
      ]))
    }))
  }
})

describe('API Smoke Tests', () => {
  test('GET /api/auth/validate', async () => {
    const res = await request(app).get('/api/auth/validate')
    expect(res.status).toBe(200)
    expect(res.body).toEqual({ ok: true, viewer: 'tester' })
  })

  test('GET /api/pins/recommendations', async () => {
    const res = await request(app).get('/api/pins/recommendations')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('items')
    expect(Array.isArray(res.body.items)).toBe(true)
  })

  test('GET /api/duplicates/scan', async () => {
    const res = await request(app).get('/api/duplicates/scan')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('pairs')
    expect(Array.isArray(res.body.pairs)).toBe(true)
  })

  test('GET /api/duplicates/content-scan', async () => {
    const res = await request(app).get('/api/duplicates/content-scan?a=repo1&b=repo2')
    expect(res.status).toBe(200)
  })
  
  test('POST /api/security/rotate', async () => {
    const res = await request(app).post('/api/security/rotate').send({ secret: 'new-secret' })
    expect(res.status).toBe(200)
    expect(res.body).toEqual({ ok: true })
  })

  test('POST /api/security/rotate missing secret', async () => {
    const res = await request(app).post('/api/security/rotate').send({})
    expect(res.status).toBe(400)
  })
})
