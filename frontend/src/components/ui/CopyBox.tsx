import { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import clsx from 'clsx'

export function CopyBox({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex items-center gap-2 bg-pink-50 border border-pink-200 rounded-xl p-4 cursor-pointer hover:bg-pink-100 transition-colors" onClick={handleCopy}>
      <div className="flex-1 font-mono text-sm overflow-x-auto whitespace-nowrap text-charcoal">
        {text}
      </div>
      <div className={clsx("p-2 rounded-lg transition-colors", copied ? "bg-emerald-100 text-emerald-600" : "bg-white text-pink-400 border border-pink-200")}>
        {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
      </div>
    </div>
  )
}
