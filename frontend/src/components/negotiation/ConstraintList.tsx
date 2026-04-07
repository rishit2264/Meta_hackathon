import React from 'react'
import { X } from 'lucide-react'
import { PrivateConstraint } from '@/types'

export function ConstraintList({ constraints, onRemove }: { constraints: PrivateConstraint[], onRemove: (id: string) => void }) {
  if (constraints.length === 0) {
    return (
      <div className="bg-pink-50 border border-pink-200 border-dashed rounded-2xl p-8 text-center text-pink-400 font-medium">
        No constraints added yet — click a template above or build your own.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {constraints.map(c => (
        <div key={c.constraint_id} className="flex items-center justify-between bg-white border border-pink-200 rounded-xl p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${c.is_deal_breaker ? 'bg-red-500' : 'bg-amber-400'}`} />
            <span className="font-medium text-charcoal">{c.description}</span>
            <span className="bg-pink-50 text-pink-600 text-xs px-2 py-1 rounded border border-pink-100 uppercase tracking-wider">{c.clause_category}</span>
            {c.is_deal_breaker && <span className="bg-red-100 text-red-600 text-[10px] font-bold px-2 py-0.5 rounded-full">DEAL-BREAKER</span>}
          </div>
          <button onClick={() => onRemove(c.constraint_id)} className="text-muted hover:text-red-500 transition-colors p-1">
            <X className="w-5 h-5" />
          </button>
        </div>
      ))}
    </div>
  )
}
