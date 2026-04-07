import { useState } from 'react'
import { Button } from '@/components/ui/Button'
import { Check } from 'lucide-react'

export function SigningBox({ companyName, role, onSign, hasSigned }: { companyName: string, role: string, onSign: () => void, hasSigned: boolean }) {
  const [signing, setSigning] = useState(false)

  const handleSign = async () => {
    setSigning(true)
    await onSign()
    setSigning(false)
  }

  return (
    <div className="bg-white border-2 border-pink-200 rounded-2xl p-6 relative overflow-hidden">
      <div className="relative z-10">
        <h3 className="font-display font-bold text-2xl text-charcoal mb-1">{companyName}</h3>
        <p className="text-slate text-sm mb-6 uppercase tracking-wider font-semibold">Representing: {role}</p>
        
        {hasSigned ? (
          <div className="bg-emerald-50 text-emerald-700 px-6 py-4 rounded-xl flex items-center justify-center gap-3 font-semibold border border-emerald-200">
            <Check className="w-5 h-5" /> Signed & Executed
          </div>
        ) : (
          <Button onClick={handleSign} isLoading={signing} className="w-full">
            Sign as {role}
          </Button>
        )}
      </div>
      
      {hasSigned && (
        <div className="absolute -bottom-6 -right-6 opacity-10 transform -rotate-12">
          <div className="w-40 h-40 border-[8px] border-emerald-500 rounded-full flex items-center justify-center">
            <span className="font-display font-bold text-4xl text-emerald-500">SEAL</span>
          </div>
        </div>
      )}
    </div>
  )
}
