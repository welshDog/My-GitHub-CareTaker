import { findDuplicates } from '../src/plugins/duplicates'
import Redis from 'ioredis-mock'
import { GitHub } from '../src/github'
import { expect, test } from '@jest/globals'

test('duplicate scan flags similar names', async ()=>{
  const gh = { reposByUser: async ()=> [
    { name:'Repo_XYZ', description:'', stargazerCount:0, forkCount:0, updatedAt:'', pushedAt:new Date().toISOString() },
    { name:'repo-xyz', description:'', stargazerCount:0, forkCount:0, updatedAt:'', pushedAt:new Date().toISOString() }
  ] } as unknown as GitHub
  const redis:any = new (Redis as any)()
  const pairs = await findDuplicates(gh, 'tester', redis)
  expect(pairs.length).toBeGreaterThan(0)
})
