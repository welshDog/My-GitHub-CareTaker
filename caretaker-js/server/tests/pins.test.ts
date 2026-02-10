import { recommendPins } from '../src/plugins/pins'
import Redis from 'ioredis-mock'
import { GitHub } from '../src/github'
import { expect, test } from '@jest/globals'

test('recommendations returns up to six items', async ()=>{
  const gh = { reposByUser: async ()=> Array.from({length:10}).map((_,i)=>({
    name:`repo${i}`, description:'hypercode', stargazerCount:i, forkCount:i/2, updatedAt:new Date().toISOString(), pushedAt:new Date().toISOString()
  })) } as unknown as GitHub
  const redis:any = new (Redis as any)()
  const items = await recommendPins(gh, 'user', redis)
  expect(items.length).toBe(6)
})
