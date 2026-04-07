'use client'
import Link from 'next/link'

export function Navbar() {
  return (
    <nav className="bg-white border-b border-pink-200 sticky top-0 z-50 px-8 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-3 h-3 rounded-full bg-pink-400" />
        <span className="font-display font-semibold text-xl tracking-tight">ContractEnv</span>
        <span className="bg-pink-50 text-pink-500 px-2 py-0.5 rounded-full text-xs font-mono ml-2">v1.0.0</span>
      </div>
      
      <div className="flex items-center gap-6">
        <Link href="/demo" className="text-sm font-medium hover:text-pink-500 transition-colors">
          Demo
        </Link>
        <Link href="/negotiate" className="bg-pink-400 text-white px-5 py-2.5 rounded-xl font-medium hover:bg-pink-500 transition-colors">
          Start Negotiation
        </Link>
      </div>
    </nav>
  )
}
