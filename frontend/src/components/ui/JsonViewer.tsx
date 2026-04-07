import React from 'react'

export function JsonViewer({ data }: { data: any }) {
  const formatValue = (val: any) => {
    if (typeof val === 'string') return <span className="text-emerald-500">"{val}"</span>
    if (typeof val === 'number') return <span className="text-amber-500">{val}</span>
    if (typeof val === 'boolean') return <span className="text-purple-500">{val ? 'true' : 'false'}</span>
    if (val === null) return <span className="text-muted">null</span>
    return JSON.stringify(val)
  }

  const renderObject = (obj: any, indent = 0) => {
    return Object.entries(obj).map(([key, value]) => (
      <div key={key} style={{ paddingLeft: `${indent * 20}px` }}>
        <span className="text-pink-500">"{key}"</span>: {
          typeof value === 'object' && value !== null
            ? <span>{'{'}
                {renderObject(value, indent + 1)}
              {'}'}</span>
            : formatValue(value)
        },
      </div>
    ))
  }

  return (
    <div className="bg-pink-50 text-charcoal p-4 rounded-xl font-mono text-xs overflow-x-auto border border-pink-200">
      {'{'}
      {renderObject(data, 1)}
      {'}'}
    </div>
  )
}
