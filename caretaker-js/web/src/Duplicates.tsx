import React, { useEffect, useState } from 'react'

export function Duplicates(){
  const [pairs,setPairs]=useState<any[]>([])
  const [loading,setLoading]=useState(false)
  async function run(){ setLoading(true); const r = await fetch('/api/duplicates/scan'); const j = await r.json(); setPairs(j.pairs); setLoading(false) }
  useEffect(()=>{ run() },[])
  return (
    <section>
      <h2>Duplicate Scan</h2>
      <button onClick={run} disabled={loading}>{loading?'Scanning…':'Run Duplicate Scan'}</button>
      <ul>
        {pairs.map((p:any)=>(<li key={`${p.a}-${p.b}`}>{p.a} ↔ {p.b} • score {p.score.toFixed(2)}</li>))}
      </ul>
    </section>
  )
}
