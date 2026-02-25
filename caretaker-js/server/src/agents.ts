import { Request, Response } from 'express'
import Redis from 'ioredis'
import { logger } from './logger'
import Bottleneck from 'bottleneck'
import { z } from 'zod'

const reviewSchema = z.object({ repo:z.string(), pr:z.number(), comment:z.string(), score:z.number().optional() })

export function agentRoutes(app:any, redis:Redis){
  app.post('/api/agents/register', async (req:Request, res:Response)=>{
    const { name, callbackUrl, token } = req.body
    if(!name || !callbackUrl){ return res.status(400).json({ error: 'missing fields' }) }
    const id = `agent:${name}`
    await redis.hmset(id, { callbackUrl, token: token ? 'stored' : '' })
    res.json({ ok:true })
  })

  app.post('/api/agents/webhook', async (req:Request, res:Response)=>{
    const event = req.body
    const priority = event.priority || 'normal'
    await redis.lpush(`agent:queue:${priority}`, JSON.stringify(event))
    res.json({ queued:true })
  })

  const limiter = new Bottleneck({ reservoir: 100, reservoirRefreshAmount: 100, reservoirRefreshInterval: 60*1000 })
  async function popQueue(){
    const levels = ['critical','high','normal','low']
    let item:string|null=null
    for(const lvl of levels){ item = await redis.rpop(`agent:queue:${lvl}`); if(item) break }
    return item
  }
  
  // FIX: Use recursive setTimeout pattern to prevent race conditions
  async function processQueue() {
    try {
      const item = await popQueue()
      if(item) {
        const e = JSON.parse(item)
        await limiter.schedule(async ()=>{
          logger.info({ event: e.action || 'repo_event' }, 'dispatching to agents')
          const review = reviewSchema.safeParse(e.review)
          if(!review.success){ await redis.lpush('agent:deadletter', item); return }
          await redis.lpush('agent:reviews', JSON.stringify(review.data))
        })
      }
    } catch(err){ 
      logger.error(err as any) 
    } finally {
      // Schedule next run only after current one finishes
      setTimeout(processQueue, 1000)
    }
  }

  // Start the loop
  processQueue()

  const reviewInterval = setInterval(async ()=>{
    const items = await redis.lrange('agent:reviews', 0, -1)
    if(items.length){ logger.info({ count: items.length }, 'aggregated reviews available') }
  }, 5000)
  
  // FIX: queueInterval is no longer used, return reviewInterval only or adapt interface
  return { queueInterval: processQueue, reviewInterval } // Assuming processQueue is what we want to expose or just null if type allows
}
