import Link from 'next/link'

export function Footer() {
  return (
    <footer className="bg-charcoal text-white py-8 text-center">
      <p className="font-display text-lg mb-2">ContractEnv — Meta/Scaler OpenEnv Hackathon 2026</p>
      <div className="flex items-center justify-center gap-4 text-sm text-pink-200 font-medium">
        <Link href="/demo" className="hover:text-white transition-colors">Demo</Link>
        <span>|</span>
        <a href="#" className="hover:text-white transition-colors">GitHub</a>
        <span>|</span>
        <a href="#" className="hover:text-white transition-colors">OpenEnv</a>
      </div>
    </footer>
  )
}
