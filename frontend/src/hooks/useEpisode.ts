import { useState, useEffect } from 'react'
import { generateSessionId, api } from '@/lib/api'
import type { EpisodeState, Action } from '@/types'

export function useEpisode() {
  const [episodeState, setEpisodeState] = useState<EpisodeState>({
    observation: null as any,
    reward: null,
    done: false,
    gradeResult: null,
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)

  const clearError = () => setError(null)

  const reset = async (taskId: string) => {
    setIsLoading(true)
    setError(null)
    try {
      const newSid = generateSessionId()
      setSessionId(newSid)
      const { data } = await api.reset(taskId, newSid)
      setEpisodeState({ observation: data.observation, reward: null, done: false, gradeResult: null })
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to reset episode')
    } finally {
      setIsLoading(false)
    }
  }

  const step = async (action: Action) => {
    if (!sessionId) return
    setIsLoading(true)
    setError(null)
    try {
      const { data } = await api.step(sessionId, action)
      setEpisodeState(prev => ({
        ...prev,
        observation: data.observation,
        reward: data.reward,
        done: data.done,
      }))
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to step')
    } finally {
      setIsLoading(false)
    }
  }

  const grade = async () => {
    if (!sessionId || !episodeState.observation) return null
    setIsLoading(true)
    setError(null)
    try {
      const { data } = await api.grade(sessionId, episodeState.observation.task_id)
      setEpisodeState(prev => ({ ...prev, gradeResult: data }))
      return data
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to grade episode')
      return null
    } finally {
      setIsLoading(false)
    }
  }

  return {
    episodeState,
    isLoading,
    error,
    sessionId,
    reset,
    step,
    grade,
    clearError,
  }
}
