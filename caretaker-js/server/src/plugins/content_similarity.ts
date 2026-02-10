import Redis from 'ioredis'
import fetch from 'node-fetch'

function tokenize(s:string){ return (s||'').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean) }
function jaccard(a:Set<string>, b:Set<string>){ const i=[...a].filter(x=>b.has(x)).length; const u = new Set([...a, ...b]).size; return u? i/u : 0 }

export async function contentSimilarity(owner:string, repoA:string, repoB:string, threshold=0.85, redis:Redis){
  const cacheKey = `content-sim:${owner}:${repoA}:${repoB}`
  const cached = await redis.get(cacheKey); if(cached) return JSON.parse(cached)
  async function sample(repo:string){
    const treeResp = await fetch(`https://api.github.com/repos/${owner}/${repo}/git/trees/main?recursive=1`, { headers:{ Authorization:`Bearer ${process.env.GH_TOKEN}` }})
    const tree:any = await treeResp.json()
    const files = (tree.tree||[]).filter((n:any)=> n.type==='blob' && /\.(ts|js|py|java)$/i.test(n.path))
    const stratified = files.filter((_:any,i:number)=> i % Math.ceil(files.length/20) === 0)
    const samples:string[]=[]
    for(const f of stratified){
      const c = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${encodeURIComponent(f.path)}?ref=main`, { headers:{ Authorization:`Bearer ${process.env.GH_TOKEN}` }})
      const cj:any = await c.json()
      if(cj && cj.content){ samples.push(Buffer.from(cj.content,'base64').toString('utf-8')) }
    }
    return samples.join('\n')
  }
  const [a,b] = await Promise.all([sample(repoA), sample(repoB)])
  const sa = new Set(tokenize(a)); const sb = new Set(tokenize(b))
  const score = jaccard(sa,sb)
  const result = { score, threshold, similar: score>=threshold }
  await redis.set(cacheKey, JSON.stringify(result), 'EX', 3600)
  return result
}
