import clsx from 'clsx'

type BadgeProps = {
  variant: 'easy'|'medium'|'hard'|'agreed'|'unfair'|'fair'|'neutral'|'pending'|'deal-breaker'
  children: React.ReactNode
  className?: string
}

export function Badge({ variant, children, className }: BadgeProps) {
  const variants = {
    easy: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    medium: 'bg-amber-100 text-amber-700 border-amber-200',
    hard: 'bg-red-100 text-red-700 border-red-200',
    agreed: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    unfair: 'bg-red-100 text-red-700 border-red-200',
    fair: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    neutral: 'bg-amber-100 text-amber-700 border-amber-200',
    pending: 'bg-pink-100 text-pink-500 border-pink-200',
    'deal-breaker': 'bg-red-100 text-red-600 border-red-200',
  }

  return (
    <span className={clsx('border rounded-full text-xs font-semibold px-3 py-1', variants[variant], className)}>
      {children}
    </span>
  )
}
