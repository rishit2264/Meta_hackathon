import clsx from 'clsx'

export function TypingIndicator({ role }: { role: 'seller_agent'|'client_agent' }) {
  const isSeller = role === 'seller_agent'

  return (
    <div className={clsx("flex gap-3 my-4", isSeller ? "justify-start" : "justify-end")}>
      {isSeller && (
        <div className="w-8 h-8 rounded-full bg-pink-400 flex items-center justify-center shadow-sm flex-shrink-0" />
      )}
      
      <div className={clsx(
        "px-5 py-4 shadow-sm flex items-center gap-1",
        isSeller ? "bg-pink-100 border border-pink-200 rounded-2xl rounded-tl-sm" : "bg-white border border-pink-200 rounded-2xl rounded-tr-sm"
      )}>
        <div className="w-1.5 h-1.5 bg-pink-400 rounded-full typing-dot" />
        <div className="w-1.5 h-1.5 bg-pink-400 rounded-full typing-dot" />
        <div className="w-1.5 h-1.5 bg-pink-400 rounded-full typing-dot" />
      </div>

      {!isSeller && (
        <div className="w-8 h-8 rounded-full bg-slate flex items-center justify-center shadow-sm flex-shrink-0" />
      )}
    </div>
  )
}
