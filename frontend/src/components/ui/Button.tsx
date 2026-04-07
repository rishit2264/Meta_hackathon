import clsx from 'clsx'

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'outline' | 'ghost' | 'danger'
  isLoading?: boolean
}

export function Button({ variant = 'primary', isLoading, className, children, disabled, ...props }: ButtonProps) {
  const variants = {
    primary: 'bg-pink-400 hover:bg-pink-500 text-white',
    outline: 'border-2 border-pink-400 text-pink-500 hover:bg-pink-50',
    ghost: 'text-pink-500 hover:bg-pink-50',
    danger: 'bg-red-100 text-red-600 hover:bg-red-200',
  }

  return (
    <button
      disabled={isLoading || disabled}
      className={clsx(
        'rounded-xl px-6 py-3 font-medium transition-all duration-200 flex items-center justify-center gap-2 outline-none focus:ring-2 focus:ring-pink-200',
        variants[variant],
        (isLoading || disabled) && 'opacity-50 cursor-not-allowed',
        className
      )}
      {...props}
    >
      {isLoading ? (
        <span className="w-5 h-5 border-2 border-t-transparent border-current rounded-full animate-spin" />
      ) : null}
      {children}
    </button>
  )
}
