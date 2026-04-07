import clsx from 'clsx'
import { Check } from 'lucide-react'

type ProgressStepsProps = {
  steps: string[]
  currentStep: number
}

export function ProgressSteps({ steps, currentStep }: ProgressStepsProps) {
  return (
    <div className="flex items-center justify-center mb-8 px-4 w-full">
      {steps.map((step, idx) => {
        const isCompleted = idx < currentStep
        const isActive = idx === currentStep
        const isFuture = idx > currentStep

        return (
          <div key={step} className="flex items-center">
            <div className="flex flex-col items-center relative">
              <div
                className={clsx(
                  "w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors",
                  isCompleted ? "bg-emerald-400 text-white" :
                  isActive ? "bg-pink-400 text-white" :
                  "border-2 border-pink-200 text-pink-300"
                )}
              >
                {isCompleted ? <Check className="w-5 h-5" /> : idx + 1}
              </div>
              <span className={clsx("absolute top-10 text-xs w-24 text-center font-medium", isActive || isCompleted ? "text-charcoal" : "text-muted")}>
                {step}
              </span>
            </div>
            {idx < steps.length - 1 && (
              <div 
                className={clsx(
                  "h-1 w-16 sm:w-32 mx-2 rounded-full transition-colors",
                  isCompleted ? "bg-emerald-400" : "bg-pink-100"
                )} 
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
