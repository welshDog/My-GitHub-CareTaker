document.querySelectorAll('button[data-plugin]').forEach(b=>{
  b.addEventListener('click', async ()=>{
    const name=b.getAttribute('data-plugin')
    const r=await fetch(`/run/${name}`)
    const j=await r.json()
    document.getElementById('result').textContent=JSON.stringify(j,null,2)
  })
})

