import { ref, watch } from 'vue'

interface CountAnimationOptions {
  duration?: number
  easing?: (t: number) => number
}

export function useCountAnimation(target: number, options: CountAnimationOptions = {}) {
  const { duration = 1000, easing = (t: number) => t * (2 - t) } = options
  const displayValue = ref(0)

  const animate = (from: number, to: number) => {
    const startTime = Date.now()
    const difference = to - from

    const step = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easedProgress = easing(progress)

      displayValue.value = Math.round(from + difference * easedProgress)

      if (progress < 1) {
        requestAnimationFrame(step)
      }
    }

    requestAnimationFrame(step)
  }

  watch(() => target, (newValue, oldValue) => {
    animate(oldValue || 0, newValue)
  }, { immediate: true })

  return { displayValue }
}
