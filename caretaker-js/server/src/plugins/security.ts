import { Request, Response } from 'express'
import { GitHub } from '../github'
import { logger } from '../logger'
import Redis from 'ioredis'

export function securityRoutes(app:any, gh:GitHub, redis:Redis, verify:any){
  app.post('/api/security/webhook', verify, async (req:Request, res:Response)=>{
    const event = req.body
    const repoFull = event?.repository?.full_name || ''
    const [owner, name] = repoFull.split('/')
    const severity = event?.alert?.security_advisory?.severity || 'unknown'
    const advisoryId = event?.alert?.security_advisory?.ghsa_id || 'unknown'
    const pkg = event?.alert?.dependency?.package?.name || ''
    const guidance = event?.alert?.security_advisory?.description || ''
    await redis.hset('security:metrics', advisoryId, JSON.stringify({ owner, name, severity }))
    try{
      const title = `[Dependabot] ${pkg} vulnerability ${advisoryId} (${severity})`
      const body = `Severity: ${severity}\n\n${guidance}\n\nAuto-created by CareTaker.`
      await gh.createIssue(owner, name, title, body)
    }catch(e){ logger.error(e as any) }
    res.json({ ok:true })
  })
  app.get('/api/security/metrics', async (_req:Request, res:Response)=>{
    const m = await redis.hgetall('security:metrics')
    const items = Object.values(m).map(v=>JSON.parse(v))
    res.json({ items })
  })
}
