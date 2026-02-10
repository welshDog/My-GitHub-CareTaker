import crypto from 'crypto'
import { Request, Response, NextFunction } from 'express'
import Redis from 'ioredis'
import { logger } from '../logger'

export function rawBodyCapture(){
  return (req: any, _res: Response, buf: Buffer) => { req.rawBody = buf }
}

export function verifySignature(redis: Redis){
  return async (req: any, res: Response, next: NextFunction) => {
    try{
      const sig = req.headers['x-hub-signature-256'] as string
      if(!sig || !sig.startsWith('sha256=')){
        logger.warn({ ts: Date.now(), ip: req.ip }, 'missing signature')
        return res.status(401).json({ error: 'missing signature' })
      }
      const hash = sig.replace('sha256=','')
      const secrets = await redis.lrange('webhook:secrets', 0, -1)
      let valid=false
      for(const s of secrets){
        const hmac = crypto.createHmac('sha256', s).update(req.rawBody || Buffer.from('')).digest('hex')
        if(crypto.timingSafeEqual(Buffer.from(hmac), Buffer.from(hash))){ valid=true; break }
      }
      if(!valid){
        logger.error({ ts: Date.now(), ip: req.ip, payload: crypto.createHash('sha256').update(req.rawBody||'').digest('hex') }, 'invalid signature')
        return res.status(401).json({ error: 'invalid signature' })
      }
      const replayKey = `replay:${hash}`
      const exists = await redis.get(replayKey)
      if(exists){ logger.error({ ts: Date.now(), ip: req.ip }, 'replay detected'); return res.status(401).json({ error: 'replay' }) }
      await redis.set(replayKey, '1', 'EX', 300)
      next()
    }catch(e){
      logger.error(e as any)
      res.status(401).json({ error: 'verification error' })
    }
  }
}

export async function rotateSecret(redis: Redis, newSecret: string){
  await redis.lpush('webhook:secrets', newSecret)
  const len = await redis.llen('webhook:secrets')
  if(len>12){ await redis.ltrim('webhook:secrets', 0, 11) }
  await redis.expire('webhook:secrets', 60*60*24*30)
}
