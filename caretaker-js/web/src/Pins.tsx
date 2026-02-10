import React, { useEffect, useState } from 'react'
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'

export function Pins(){
  const [items,setItems]=useState<any[]>([])
  useEffect(()=>{ fetch('/api/pins/recommendations').then(r=>r.json()).then(d=>setItems(d.items)) },[])
  function onDragEnd(result:any){
    if(!result.destination) return
    const arr = Array.from(items)
    const [moved] = arr.splice(result.source.index,1)
    arr.splice(result.destination.index,0,moved)
    setItems(arr)
  }
  return (
    <section>
      <h2>Pins</h2>
      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="pins" direction="horizontal">
          {(provided)=> (
            <div ref={provided.innerRef} {...provided.droppableProps} style={{display:'flex',gap:12,flexWrap:'wrap'}}>
              {items.map((it,idx)=> (
                <Draggable key={it.name} draggableId={it.name} index={idx}>
                  {(p)=> (
                    <div ref={p.innerRef} {...p.draggableProps} {...p.dragHandleProps} style={{border:'1px solid #ccc',padding:12,borderRadius:8,minWidth:220}}>
                      <strong>{it.name}</strong>
                      <div>⭐ {it.stargazerCount} • 🍴 {it.forkCount}</div>
                      <div>Updated {it.updatedAt}</div>
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </section>
  )
}
