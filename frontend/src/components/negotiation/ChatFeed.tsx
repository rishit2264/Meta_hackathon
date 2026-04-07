import React, { useEffect, useRef } from 'react'
import { ChatBubble } from './ChatBubble'
import { TypingIndicator } from './TypingIndicator'
import { NegotiationTurn } from '@/types'

export function ChatFeed({ turns, isComplete, nextSpeaker }: { turns: NegotiationTurn[], isComplete: boolean, nextSpeaker?: 'seller_agent'|'client_agent' }) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [turns, isComplete, nextSpeaker])

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
      {turns.map((t, i) => (
        <ChatBubble 
          key={i} 
          role={t.speaker} 
          message={t.content} 
          meta={{ clause_id: t.clause_id, action_type: t.action_type, turn_number: t.turn_number, proposed_text: t.proposed_text }} 
        />
      ))}
      {!isComplete && nextSpeaker && <TypingIndicator role={nextSpeaker} />}
      <div ref={bottomRef} />
    </div>
  )
}
