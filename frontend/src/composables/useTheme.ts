import { ref, watch } from 'vue'

type Theme = 'light' | 'dark'

const theme = ref<Theme>('light')
const THEME_KEY = 'asset-manager-theme'
let initialized = false

// 테마 적용
const applyTheme = (newTheme: Theme) => {
  if (newTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 초기 테마 로드
const initTheme = () => {
  if (initialized) return

  const savedTheme = localStorage.getItem(THEME_KEY) as Theme | null
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme) {
    theme.value = savedTheme
  } else if (prefersDark) {
    theme.value = 'dark'
  }

  applyTheme(theme.value)
  initialized = true
}

// 테마 변경 감지 및 저장
watch(theme, (newTheme) => {
  applyTheme(newTheme)
  localStorage.setItem(THEME_KEY, newTheme)
})

export function useTheme() {
  // 첫 호출 시 초기화
  initTheme()

  // 테마 토글
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  // 테마 설정
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
  }

  return {
    theme,
    toggleTheme,
    setTheme,
    isDark: () => theme.value === 'dark'
  }
}
