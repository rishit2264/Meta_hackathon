import { Clause } from '@/types'
import clsx from 'clsx'
import { Check } from 'lucide-react'

export function ClauseTabBar({ clauses, activeId, onChange }: { clauses: Clause[], activeId: string, onChange: (id: string) => void }) {
  return (
    <div className="flex px-4 py-2 gap-2 border-b border-pink-200 bg-white/50 backdrop-blur overflow-x-auto">
      {clauses.map(c => {
        const isActive = c.id === activeId
        const isAgreed = c.status === 'agreed'
        
        return (
          <button
            key={c.id}
            onClick={() => onChange(c.id)}
            className={clsx(
              "px-4 py-2 rounded-lg text-sm font-semibold transition-colors flex items-center gap-2 whitespace-nowrap",
              isActive ? "bg-pink-400 text-white shadow-sm" : 
              isAgreed ? "bg-emerald-50 text-emerald-700 hover:bg-emerald-100" : 
              "bg-pink-50 text-pink-500 hover:bg-pink-100"
            )}
          >
            {isAgreed && <Check className="w-3.5 h-3.5" />}
            {c.title}
          </button>
        )
      })}
    </div>
  )
}
