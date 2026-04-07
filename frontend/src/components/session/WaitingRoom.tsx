import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { LiveBadge } from '@/components/ui/LiveBadge'

export function WaitingRoom({ sessionId, onReady }: { sessionId: string, onReady: () => void }) {
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const { data } = await api.session.status(sessionId)
        if (data.status === 'ready' || data.status === 'negotiating') {
          clearInterval(interval)
          onReady()
        }
      } catch (err) {}
    }, 3000)
    return () => clearInterval(interval)
  }, [sessionId, onReady])

  return (
    <div className="bg-white border text-charcoal border-pink-200 rounded-2xl p-8 max-w-md mx-auto shadow-sm text-center flex flex-col items-center">
      <LiveBadge className="mb-6" />
      <h2 className="font-display font-bold text-xl mb-2">Waiting for client...</h2>
      <p className="text-slate text-sm">The negotiation will begin automatically once the client configures their constraints and joins.</p>
    </div>
  )
}
