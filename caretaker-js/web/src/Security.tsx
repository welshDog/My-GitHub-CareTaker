import React, { useEffect, useState } from 'react'

export function Security(){
  const [items,setItems]=useState<any[]>([])
  useEffect(()=>{ fetch('/api/security/metrics').then(r=>r.json()).then(d=>setItems(d.items||[])) },[])
  return (
    <section>
      <h2>Security</h2>
      <table><thead><tr><th>Repo</th><th>Severity</th></tr></thead>
      <tbody>
        {items.map((i:any,idx)=>(<tr key={idx}><td>{i.owner}/{i.name}</td><td>{i.severity}</td></tr>))}
      </tbody></table>
    </section>
  )
}
