import { CopyBox } from '@/components/ui/CopyBox'

export function InviteCard({ inviteUrl }: { inviteUrl: string }) {
  return (
    <div className="bg-white border text-charcoal border-pink-200 rounded-2xl p-8 max-w-md mx-auto shadow-sm text-center">
      <div className="w-16 h-16 bg-emerald-100 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h2 className="font-display font-bold text-2xl mb-2">Session Ready!</h2>
      <p className="text-slate mb-6 text-sm">Send this secure link to the other party. They will set their own private constraints before joining.</p>
      
      <div className="text-left mb-6">
        <label className="text-xs font-semibold text-slate mb-2 block uppercase tracking-wider">Invite Link</label>
        <CopyBox text={inviteUrl} />
      </div>
    </div>
  )
}
