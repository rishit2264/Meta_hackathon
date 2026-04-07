import { PrivateConstraint } from '@/types'

export function PrivateConstraintPanel({ constraints }: { constraints: PrivateConstraint[] }) {
  if (!constraints || constraints.length === 0) return null
  
  return (
    <div className="mt-4">
      <h3 className="text-xs font-bold tracking-widest uppercase text-pink-400 mb-4">Your Private Rules</h3>
      <div className="space-y-3">
        {constraints.map(c => (
          <div key={c.constraint_id} className="bg-pink-50 border border-pink-200 rounded-xl p-3">
            <div className="flex items-start gap-2">
              <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${c.is_deal_breaker ? 'bg-red-500' : 'bg-amber-400'}`} />
              <div>
                <p className="text-xs font-medium text-charcoal">{c.description}</p>
                <p className="text-[10px] text-muted uppercase tracking-wider mt-1">{c.clause_category} • {c.rule_type}</p>
              </div>
            </div>
            {/* Note: "Satisfied / At Risk" status requires deeper parsing in a real prod app, mocked pending here */}
            <div className="mt-2 text-right">
              <span className="text-[10px] font-semibold text-muted">PENDING...</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
