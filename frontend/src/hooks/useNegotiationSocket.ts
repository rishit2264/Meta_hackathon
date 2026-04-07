import { useState, useEffect } from 'react'
import { NegotiationTurn } from '@/types'
import { WS_URL } from '@/lib/api'

export function useNegotiationSocket(sessionId: string, role: string) {
  const [turns, setTurns] = useState<NegotiationTurn[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [isComplete, setIsComplete] = useState(false)
  const [latestTurn, setLatestTurn] = useState<NegotiationTurn | null>(null)

  useEffect(() => {
    if (!sessionId || !role) return

    let timeoutId: any;
    let ws: WebSocket;

    const connect = () => {
      ws = new WebSocket(WS_URL(sessionId, role))
      
      ws.onopen = () => {
        setIsConnected(true)
      }
      
      ws.onmessage = (e) => {
        try {
          const turn: NegotiationTurn = JSON.parse(e.data)
          setTurns(prev => [...prev, turn])
          setLatestTurn(turn)
          if (turn.speaker === 'system' && turn.content.includes('complete')) {
            setIsComplete(true)
          }
        } catch (err) {
          console.error("Failed to parse websocket message", err, e.data)
        }
      }
      
      ws.onclose = () => {
        setIsConnected(false)
        timeoutId = setTimeout(connect, 3000)
      }
    }

    connect()

    return () => {
      clearTimeout(timeoutId)
      if (ws) {
        ws.onclose = null
        ws.close()
      }
    }
  }, [sessionId, role])

  return { turns, isConnected, isComplete, latestTurn }
}
