'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'
import { SigningBox } from '@/components/session/SigningBox'
import { api } from '@/lib/api'
import { CheckCircle } from 'lucide-react'

export default function SignPage({ params }: { params: { sessionId: string } }) {
  const router = useRouter()
  const [session, setSession] = useState<any>(null)
  const [finalContract, setFinalContract] = useState<any>(null)

  useEffect(() => {
    // Poll for status
    const fetchSession = async () => {
      try {
        const { data } = await api.session.status(params.sessionId)
        setSession(data)
        if (data.seller_signed && data.client_signed) {
          const contractReq = await api.session.contract(params.sessionId)
          setFinalContract(contractReq.data)
        }
      } catch(e) {}
    }
    fetchSession()
    const int = setInterval(fetchSession, 3000)
    return () => clearInterval(int)
  }, [params.sessionId])

  const handleSign = async (role: string) => {
    await api.session.sign(params.sessionId, role)
  }

  if (!session) return null

  const bothSigned = session.seller_signed && session.client_signed

  return (
    <div className="min-h-screen flex flex-col bg-pink-50">
      <Navbar />
      
      <main className="flex-1 py-12 px-4 max-w-5xl mx-auto w-full">
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-emerald-100 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
            <CheckCircle className="w-10 h-10" />
          </div>
          <h1 className="font-display font-bold text-4xl text-charcoal mb-4">Negotiation Complete</h1>
          <p className="text-slate text-lg max-w-2xl mx-auto">Review the agreed contract below and sign to execute the agreement.</p>
        </div>

        {/* Stats Row */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white border border-pink-200 rounded-2xl p-6 text-center shadow-sm">
            <p className="text-sm font-semibold text-slate uppercase tracking-widest mb-1">Clauses Agreed</p>
            <p className="font-display font-bold text-3xl text-pink-500">{Object.keys(session.final_agreed_clauses || {}).length} / {session.clauses?.length}</p>
          </div>
          <div className="bg-white border border-pink-200 rounded-2xl p-6 text-center shadow-sm">
            <p className="text-sm font-semibold text-slate uppercase tracking-widest mb-1">Total Turns</p>
            <p className="font-display font-bold text-3xl text-pink-500">{session.turn}</p>
          </div>
          <div className="bg-white border border-pink-200 rounded-2xl p-6 text-center shadow-sm">
            <p className="text-sm font-semibold text-slate uppercase tracking-widest mb-1">Time Elapsed</p>
            <p className="font-display font-bold text-3xl text-pink-500 font-mono">1m 45s</p>
          </div>
        </div>

        {/* Final Contract Viewer */}
        <div className="bg-white border border-pink-200 rounded-3xl p-10 mb-12 shadow-sm text-charcoal">
          <h2 className="font-display font-bold text-3xl mb-8 text-center">{session.contract_title}</h2>
          
          <div className="space-y-8">
            {session.clauses?.map((c: any) => {
              const agreedText = session.final_agreed_clauses?.[c.id]
              return (
                <div key={c.id} className="space-y-3">
                  <h4 className="font-display font-bold text-lg">{c.title}</h4>
                  
                  {agreedText ? (
                    <>
                      <p className="text-sm text-muted line-through leading-relaxed">{c.text}</p>
                      <div className="bg-emerald-50 border-l-4 border-emerald-400 p-4 rounded-r-xl">
                        <p className="text-sm font-medium leading-relaxed">{agreedText}</p>
                      </div>
                    </>
                  ) : (
                    <p className="text-sm leading-relaxed">{c.text}</p>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Signing Area */}
        {bothSigned && (
          <div className="bg-emerald-50 border-2 border-emerald-400 rounded-2xl p-6 text-center mb-12 shadow-sm">
            <h3 className="font-display font-bold text-2xl text-emerald-700 flex items-center justify-center gap-3">
              <CheckCircle /> Contract Executed
            </h3>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <SigningBox 
            companyName={session.seller_config?.company_name || 'Seller'}
            role="Seller"
            hasSigned={session.seller_signed}
            onSign={() => handleSign('seller')}
          />
          <SigningBox 
            companyName={session.client_config?.company_name || 'Client'}
            role="Client"
            hasSigned={session.client_signed}
            onSign={() => handleSign('client')}
          />
        </div>

        {bothSigned && (
          <div className="text-center pb-24">
            <button 
              onClick={() => {
                const blob = new Blob([finalContract?.final_contract_text || JSON.stringify(session, null, 2)], { type: 'text/plain' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = 'contract.txt'
                a.click()
              }} 
              className="bg-charcoal text-white px-8 py-4 rounded-xl font-medium hover:bg-slate transition-colors mr-4"
            >
              Download Final Contract
            </button>
            <button 
              onClick={() => router.push('/negotiate')} 
              className="bg-white border-2 border-pink-400 text-pink-500 px-8 py-4 rounded-xl font-medium hover:bg-pink-50 transition-colors"
            >
              Start Another Negotiation &rarr;
            </button>
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  )
}
