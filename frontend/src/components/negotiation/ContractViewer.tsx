import { Clause } from '@/types'
import clsx from 'clsx'

export function ContractViewer({ clauses }: { clauses: Clause[] }) {
  return (
    <div className="bg-white border text-charcoal border-pink-200 rounded-2xl p-8 max-w-3xl mx-auto shadow-sm">
      <h2 className="font-display font-bold text-3xl mb-8 text-center">Non-Disclosure Agreement</h2>
      <div className="space-y-6">
        {clauses.map(c => {
          const isAgreed = c.status === 'agreed'
          return (
            <div key={c.id} className="space-y-2">
              <h4 className="font-semibold">{c.title}</h4>
              <p className={clsx("text-sm leading-relaxed", c.current_proposed_text && "line-through text-muted")}>
                {c.text}
              </p>
              {c.current_proposed_text && (
                <div className={clsx("p-3 rounded-xl text-sm font-medium leading-relaxed border-l-4", isAgreed ? "bg-emerald-50 border-emerald-400" : "bg-pink-50 border-pink-400")}>
                  {c.current_proposed_text}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
