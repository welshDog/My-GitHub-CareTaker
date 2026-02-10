import crypto from 'crypto'
import { rawBodyCapture, verifySignature } from '../src/middleware/signature'
import Redis from 'ioredis-mock'
import { test } from '@jest/globals'

function sign(secret:string, body:Buffer){
  return 'sha256=' + crypto.createHmac('sha256', secret).update(body).digest('hex')
}

test('valid signature passes', async ()=>{
  const redis:any = new (Redis as any)()
  await redis.lpush('webhook:secrets','s1')
  const body = Buffer.from(JSON.stringify({a:1}))
  const req:any = { headers: { 'x-hub-signature-256': sign('s1', body) }, rawBody: body }

  let called=false
  const res:any = { status: (_c:number)=>({ json: (_o:any)=>{} }), json: (_o:any)=>{} }
  await verifySignature(redis)(req, res, ()=>{ called=true })
  if(!called) throw new Error('expected middleware to call next()')
})

test('invalid signature blocked', async ()=>{
  const redis:any = new (Redis as any)()
  await redis.lpush('webhook:secrets','s1')
  const body = Buffer.from(JSON.stringify({a:1}))
  const req:any = { headers: { 'x-hub-signature-256': sign('wrong', body) }, rawBody: body }
  let status:number|undefined; let payload:any
  const res:any = { status:(c:number)=>({ json: (o:any)=>{ status=c; payload=o } }), json:(o:any)=>{ payload=o } }
  await verifySignature(redis)(req, res, ()=>{})
  if(status !== 401) throw new Error(`Expected status 401, got ${status}`)
})

test('replay detected', async ()=>{
  const redis:any = new (Redis as any)()
  await redis.lpush('webhook:secrets','s1')
  const body = Buffer.from(JSON.stringify({a:1}))
  const sig = sign('s1', body)
  const req:any = { headers: { 'x-hub-signature-256': sig }, rawBody: body }
  let status:number|undefined
  const res:any = { status:(c:number)=>({ json: (o:any)=>{ status=c } }), json:(o:any)=>{} }
  await verifySignature(redis)(req, res, ()=>{})
  await verifySignature(redis)(req, res, ()=>{})
  if (status !== 401) throw new Error(`Expected status 401, got ${status}`)
})
