import { Clause } from '@/types'
import { Badge } from '@/components/ui/Badge'
import clsx from 'clsx'

export function ClauseCard({ clause, isActive, onClick }: { clause: Clause, isActive?: boolean, onClick?: () => void }) {
  const isAgreed = clause.status === 'agreed'
  
  return (
    <div 
      onClick={onClick}
      className={clsx(
        "border rounded-2xl p-5 mb-4 transition-all",
        isActive ? "border-pink-400 shadow-md ring-2 ring-pink-100 bg-white" : "border-pink-200 bg-white hover:border-pink-300 hover:shadow-sm cursor-pointer",
        isAgreed && "border-emerald-200 bg-emerald-50/30"
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h4 className="font-display font-semibold text-lg text-charcoal">{clause.title}</h4>
          <span className="text-xs font-mono text-muted uppercase tracking-wider">{clause.id} — {clause.category}</span>
        </div>
        <div className="flex gap-2">
          {clause.is_deal_breaker && <Badge variant="deal-breaker">DEAL-BREAKER</Badge>}
          {isAgreed && <Badge variant="agreed">AGREED</Badge>}
        </div>
      </div>
      
      <div className="text-sm space-y-3">
        <p className={clsx("leading-relaxed", clause.current_proposed_text && "line-through text-muted")}>
          {clause.text}
        </p>
        
        {clause.current_proposed_text && (
          <div className={clsx("p-3 rounded-xl font-medium leading-relaxed border-l-4", isAgreed ? "bg-emerald-50 border-emerald-400 text-charcoal" : "bg-pink-50 border-pink-400 text-charcoal")}>
            {clause.current_proposed_text}
          </div>
        )}
      </div>
    </div>
  )
}
