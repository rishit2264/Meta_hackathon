import clsx from 'clsx'

export function LiveBadge({ className }: { className?: string }) {
  return (
    <div className={clsx("flex items-center gap-2 bg-pink-100 text-pink-500 rounded-full px-3 py-1 text-xs font-semibold", className)}>
      <div className="w-2 h-2 rounded-full bg-pink-400 pulse-pink" />
      LIVE
    </div>
  )
}
