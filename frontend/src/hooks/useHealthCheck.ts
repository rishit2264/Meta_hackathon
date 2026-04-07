import { useState, useEffect } from 'react'
import { api } from '@/lib/api'

export function useHealthCheck() {
  const [isOnline, setIsOnline] = useState(false)
  const [version, setVersion] = useState<string | null>(null)

  useEffect(() => {
    let interval: any;

    const check = async () => {
      try {
        const { data } = await api.health()
        setIsOnline(data.status === 'ok')
        setVersion(data.version)
      } catch (err) {
        setIsOnline(false)
      }
    }

    check()
    interval = setInterval(check, 30000)

    return () => clearInterval(interval)
  }, [])

  return { isOnline, version }
}
