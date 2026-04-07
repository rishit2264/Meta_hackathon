'use client'

import React, { useState } from 'react'
import { Clause, Action } from '@/types'
import { Flag, Edit3, Check, X, ArrowRight } from 'lucide-react'

interface ActionPanelProps {
  selectedClause: Clause | null
  taskId: string
  onAction: (action: Action) => void
  isLoading?: boolean
}

const LABEL_OPTIONS = ['fair', 'unfair', 'neutral'] as const
const ACTION_TYPES = {
  task1: ['flag'],
  task2: ['propose', 'flag'],
  task3: ['accept', 'reject', 'propose', 'counter'],
}

export default function ActionPanel({
  selectedClause,
  taskId,
  onAction,
  isLoading = false,
}: ActionPanelProps) {
  const [actionType, setActionType] = useState<string>('flag')
  const [label, setLabel] = useState<string>('unfair')
  const [reason, setReason] = useState('')
  const [proposedText, setProposedText] = useState('')

  if (!selectedClause) {
    return (
      <div className="bg-white rounded-2xl border border-pink-200 p-6 text-center">
        <p className="text-sm text-muted">Select a clause to take action</p>
      </div>
    )
  }

  const availableActions = ACTION_TYPES[taskId as keyof typeof ACTION_TYPES] || ['flag']

  const handleSubmit = () => {
    if (!selectedClause) return
    const action: Action = {
      clause_id: selectedClause.id,
      action_type: actionType as any,
      label: label as any,
      reason: reason || undefined,
      proposed_text: proposedText || undefined,
    }
    onAction(action)
    setProposedText('')
    setReason('')
  }

  return (
    <div className="bg-white rounded-2xl border border-pink-200 p-5">
      <p className="text-xs font-semibold tracking-widest uppercase text-pink-400 mb-4">
        Action for [{selectedClause.id}] {selectedClause.title}
      </p>

      {/* Action type */}
      <div className="flex flex-wrap gap-2 mb-4">
        {availableActions.map(at => (
          <button
            key={at}
            onClick={() => setActionType(at)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
              actionType === at
                ? 'bg-pink-400 text-white'
                : 'bg-pink-50 text-pink-500 border border-pink-200 hover:bg-pink-100'
            }`}
          >
            {at === 'flag' && <Flag className="w-3 h-3" />}
            {at === 'propose' && <Edit3 className="w-3 h-3" />}
            {at === 'accept' && <Check className="w-3 h-3" />}
            {at === 'reject' && <X className="w-3 h-3" />}
            {at === 'counter' && <ArrowRight className="w-3 h-3" />}
            {at}
          </button>
        ))}
      </div>

      {/* Label (for flag) */}
      {(actionType === 'flag') && (
        <div className="mb-4">
          <label className="text-xs text-muted block mb-2">Assessment</label>
          <div className="flex gap-2">
            {LABEL_OPTIONS.map(l => (
              <button
                key={l}
                onClick={() => setLabel(l)}
                className={`flex-1 py-2 rounded-xl text-xs font-semibold transition-all ${
                  label === l
                    ? l === 'fair'
                      ? 'bg-emerald-100 text-emerald-700 border-2 border-emerald-400'
                      : l === 'unfair'
                      ? 'bg-red-100 text-red-600 border-2 border-red-400'
                      : 'bg-amber-100 text-amber-700 border-2 border-amber-400'
                    : 'bg-pink-50 text-muted border border-pink-200 hover:bg-pink-100'
                }`}
              >
                {l}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Reason */}
      <div className="mb-4">
        <label className="text-xs text-muted block mb-2">Reason (optional)</label>
        <input
          type="text"
          value={reason}
          onChange={e => setReason(e.target.value)}
          placeholder="Brief reason..."
          className="w-full border border-pink-200 rounded-xl px-3 py-2 text-sm focus:border-pink-400 focus:ring-2 focus:ring-pink-100 outline-none"
        />
      </div>

      {/* Proposed text */}
      {(actionType === 'propose' || actionType === 'counter') && (
        <div className="mb-4">
          <label className="text-xs text-muted block mb-2">Proposed Revision</label>
          <textarea
            value={proposedText}
            onChange={e => setProposedText(e.target.value)}
            placeholder="Write your improved clause text here..."
            rows={4}
            className="w-full border border-pink-200 rounded-xl px-3 py-2 text-sm focus:border-pink-400 focus:ring-2 focus:ring-pink-100 outline-none resize-none"
          />
        </div>
      )}

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={isLoading}
        className="w-full bg-pink-400 text-white rounded-xl py-3 text-sm font-semibold hover:bg-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        ) : (
          <>
            Submit Action
            <ArrowRight className="w-4 h-4" />
          </>
        )}
      </button>
    </div>
  )
}
