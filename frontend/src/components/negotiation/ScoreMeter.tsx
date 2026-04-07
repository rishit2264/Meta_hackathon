import React, { useEffect, useState } from 'react'

export function ScoreMeter({ label, value }: { label: string, value: number }) {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // animate on mount
    const timer = setTimeout(() => {
      setWidth(value * 100)
    }, 100)
    return () => clearTimeout(timer)
  }, [value])

  const color = label.includes('Agreement') ? 'bg-emerald-400' : 'bg-pink-400'

  return (
    <div className="mb-4">
      <div className="flex justify-between text-xs font-semibold mb-1 text-slate">
        <span>{label}</span>
        <span>{Math.round(value * 100)}%</span>
      </div>
      <div className="h-1.5 w-full bg-pink-100 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-700 ease-out rounded-full ${color}`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  )
}
