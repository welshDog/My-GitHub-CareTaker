import React, { useEffect, useState } from 'react'
import { Pins } from './Pins'
import { Duplicates } from './Duplicates'
import { Security } from './Security'

export default function App(){
  const [auth,setAuth]=useState<any>()
  useEffect(()=>{ fetch('/api/auth/validate').then(r=>r.json()).then(setAuth) },[])
  return (
    <div style={{fontFamily:'system-ui',padding:16}}>
      <h1>GitHub CareTaker</h1>
      {!auth?.ok && <div style={{color:'red'}}>Token invalid or missing</div>}
      <Security/>
      <Pins/>
      <Duplicates/>
    </div>
  )
}
