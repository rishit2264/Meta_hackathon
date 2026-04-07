'use client'

import Link from 'next/link'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { Lock, MessageSquare, PenTool, CheckCircle } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main className="flex-1">
        {/* HERO SECTION */}
        <section className="bg-cream py-24 px-8 text-center relative overflow-hidden">
          {/* Soft decorative element */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-100 rounded-full blur-[100px] opacity-60 pointer-events-none" />
          
          <div className="relative z-10 max-w-4xl mx-auto">
            <span className="inline-block bg-pink-100 text-pink-600 px-4 py-1.5 rounded-full text-sm font-semibold tracking-wide mb-6">
              Built for Meta/Scaler OpenEnv Hackathon 2026
            </span>
            <h1 className="font-display font-bold text-6xl tracking-tight text-charcoal mb-4">
              AI Negotiation.<br />
              <span className="text-pink-500">Both sides win.</span>
            </h1>
            <p className="font-sans text-xl text-slate max-w-2xl mx-auto mb-10 leading-relaxed">
              Each company sets private rules. Two AI agents negotiate autonomously. Neither sees the other's constraints.
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link href="/negotiate" className="bg-pink-400 text-white px-8 py-4 rounded-xl font-medium hover:bg-pink-500 transition-colors shadow-lg shadow-pink-200">
                Start a Negotiation &rarr;
              </Link>
              <Link href="/demo" className="border-2 border-pink-400 text-pink-500 px-8 py-4 rounded-xl font-medium hover:bg-pink-50 transition-colors">
                Try the Demo
              </Link>
            </div>
          </div>
        </section>

        {/* HOW IT WORKS SECTION */}
        <section className="bg-white py-24 px-8">
          <div className="max-w-6xl mx-auto text-center">
            <span className="text-xs font-bold tracking-widest uppercase text-pink-400 mb-2 block">How It Works</span>
            <h2 className="font-display font-bold text-4xl mb-16">Negotiation the way it should work</h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              {/* Step 1 */}
              <div className="bg-pink-50 border border-pink-200 rounded-3xl p-8 text-left transition-transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center text-pink-500 mb-6">
                  <Lock className="w-6 h-6" />
                </div>
                <h3 className="font-display font-bold text-xl mb-3">1. Set Your Rules</h3>
                <p className="text-slate leading-relaxed">
                  Upload a contract. Set your private deal-breakers, liability caps, and payment terms. The other side never sees these.
                </p>
              </div>

              {/* Step 2 */}
              <div className="bg-pink-50 border border-pink-200 rounded-3xl p-8 text-left transition-transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center text-pink-500 mb-6">
                  <MessageSquare className="w-6 h-6" />
                </div>
                <h3 className="font-display font-bold text-xl mb-3">2. Agents Negotiate</h3>
                <p className="text-slate leading-relaxed">
                  Two AI agents argue clause by clause on your behalf — live, in real time. Each agent defends its client's private constraints.
                </p>
              </div>

              {/* Step 3 */}
              <div className="bg-pink-50 border border-pink-200 rounded-3xl p-8 text-left transition-transform hover:-translate-y-1">
                <div className="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center text-pink-500 mb-6">
                  <PenTool className="w-6 h-6" />
                </div>
                <h3 className="font-display font-bold text-xl mb-3">3. Sign the Agreement</h3>
                <p className="text-slate leading-relaxed">
                  The final contract is presented. Both parties review and sign. A real, executable agreement — negotiated in minutes.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* KEY FEATURE SECTION */}
        <section className="bg-pink-50 py-24 px-8">
          <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
            <div>
              <span className="text-xs font-bold tracking-widest uppercase text-pink-400 mb-2 block">The Key Feature</span>
              <h2 className="font-display font-bold text-4xl mb-6">Private Constraints</h2>
              <p className="text-slate text-lg mb-8 leading-relaxed">
                Each company fills a simple form before negotiation. Things like 'never agree to liability over $50k' or 'payment must be net-30'. The AI agent knows these rules internally and argues from them. The opposing agent never sees them. This is what makes it feel like a real negotiation.
              </p>
              <ul className="space-y-4">
                <li className="flex items-center gap-3 text-charcoal font-medium">
                  <div className="w-1.5 h-1.5 rounded-full bg-pink-400" /> Never exposed to the opposing party
                </li>
                <li className="flex items-center gap-3 text-charcoal font-medium">
                  <div className="w-1.5 h-1.5 rounded-full bg-pink-400" /> Agent enforces them automatically
                </li>
                <li className="flex items-center gap-3 text-charcoal font-medium">
                  <div className="w-1.5 h-1.5 rounded-full bg-pink-400" /> Deal-breakers halt negotiation if violated
                </li>
              </ul>
            </div>
            
            <div className="relative">
              <div className="bg-white rounded-3xl border border-pink-200 p-8 shadow-sm">
                <h3 className="font-display font-bold text-xl mb-6 flex items-center gap-2">
                  <Lock className="w-5 h-5 text-pink-400" /> Your Private Constraints
                </h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 bg-red-50 text-red-700 px-4 py-3 rounded-xl border border-red-100 text-sm font-medium">
                    <div className="w-2 h-2 rounded-full bg-red-500" /> Non-compete: max 1 year
                  </div>
                  <div className="flex items-center gap-3 bg-amber-50 text-amber-700 px-4 py-3 rounded-xl border border-amber-100 text-sm font-medium">
                    <div className="w-2 h-2 rounded-full bg-amber-500" /> IP: carve-out for pre-existing tech
                  </div>
                  <div className="flex items-center gap-3 bg-emerald-50 text-emerald-700 px-4 py-3 rounded-xl border border-emerald-100 text-sm font-medium">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" /> Prefer Delaware jurisdiction
                  </div>
                </div>
              </div>
              {/* Blur Overlay matching prompt */}
              <div className="absolute inset-y-0 right-0 w-1/2 bg-white/60 backdrop-blur-[2px] rounded-r-3xl flex items-center justify-center border-l border-white/20">
                <div className="bg-charcoal text-white text-xs px-4 py-2 rounded-full shadow-lg flex items-center gap-2">
                  <Lock className="w-3 h-3" /> Hidden from other party
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* OPENENV COMPLIANCE */}
        <section className="bg-white py-24 px-8 text-center border-b border-pink-200">
          <div className="w-16 h-16 bg-pink-50 border-2 border-pink-200 rounded-2xl mx-auto flex items-center justify-center mb-6 transform rotate-12">
            <CheckCircle className="w-8 h-8 text-pink-400 -rotate-12" />
          </div>
          <h2 className="font-display font-bold text-3xl mb-4">Built on OpenEnv</h2>
          <p className="text-slate mb-10">The standard for reliable RL continuous environments.</p>
          <div className="flex flex-wrap justify-center gap-4 mb-10">
            <span className="px-4 py-2 rounded-full bg-pink-50 text-pink-600 font-medium text-sm">3 Standard Tasks</span>
            <span className="px-4 py-2 rounded-full bg-pink-50 text-pink-600 font-medium text-sm">Deterministic Graders</span>
            <span className="px-4 py-2 rounded-full bg-pink-50 text-pink-600 font-medium text-sm">HF Spaces Deployed</span>
          </div>
          <Link href="/demo" className="text-pink-500 font-medium hover:underline inline-flex items-center gap-1">
            Explore OpenEnv Features &rarr;
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  )
}
