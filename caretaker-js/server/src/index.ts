import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import Redis from 'ioredis'
import { config } from './config'
import { GitHub } from './github'
import { logger } from './logger'
import { securityRoutes } from './plugins/security'
import { rawBodyCapture, verifySignature, rotateSecret } from './middleware/signature'
import { recommendPins } from './plugins/pins'
import { findDuplicates } from './plugins/duplicates'
import { contentSimilarity } from './plugins/content_similarity'
import { agentRoutes } from './agents'

const app = express()
app.use(cors())
app.use(bodyParser.json({ limit: '2mb', verify: rawBodyCapture() }))

const redis = new Redis(config.redisUrl)
const gh = new GitHub(config.token)

app.get('/api/auth/validate', async (_req, res)=>{
  try{ const v:any = await gh.viewer(); res.json({ ok:true, viewer:v.viewer.login }) }
  catch(e){ res.status(401).json({ ok:false, error:'invalid token'}) }
})

app.get('/api/pins/recommendations', async (_req, res)=>{
  const data = await recommendPins(gh, config.username, redis)
  res.json({ items: data })
})

app.get('/api/duplicates/scan', async (_req, res)=>{
  const data = await findDuplicates(gh, config.username, redis)
  res.json({ pairs: data })
})

app.get('/api/duplicates/content-scan', async (req, res)=>{
  const { a, b } = req.query as any
  const data = await contentSimilarity(config.username, a, b, 0.85, redis)
  res.json(data)
})

app.post('/api/security/rotate', async (req, res)=>{
  const { secret } = req.body
  if(!secret) return res.status(400).json({ error: 'missing secret' })
  await rotateSecret(redis, secret)
  res.json({ ok:true })
})
securityRoutes(app, gh, redis, verifySignature(redis))
agentRoutes(app, redis)

export { app }

if (require.main === module) {
  app.listen(config.port, ()=> logger.info({ port: config.port }, 'server started'))
}
