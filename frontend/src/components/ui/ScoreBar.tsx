'use client'

import React, { useEffect, useState } from 'react'
import clsx from 'clsx'

export function ScoreBar({ value, targetScore }: { value: number, targetScore: number }) {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // animate on mount
    const timer = setTimeout(() => {
      setWidth(Math.max(0, Math.min(100, (value + 1) / 2 * 100))) // Map [-1, 1] to [0, 100]
    }, 100)
    return () => clearTimeout(timer)
  }, [value])

  const getColor = () => {
    if (value >= targetScore) return 'bg-emerald-400'
    if (value >= targetScore * 0.8) return 'bg-amber-400'
    return 'bg-red-400'
  }

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs font-mono mb-1 text-charcoal">
        <span>Score: {value.toFixed(2)}</span>
        <span className="text-muted">Target: {targetScore.toFixed(2)}</span>
      </div>
      <div className="h-2 w-full bg-pink-100 rounded-full overflow-hidden">
        <div 
          className={clsx('h-full transition-all duration-700 ease-out rounded-full', getColor())}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  )
}
