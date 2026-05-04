import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const isLoggedIn = computed(() => !!token.value)

  function login(user: string, pass: string): boolean {
    // MVP: mock authentication
    if (user && pass) {
      token.value = btoa(`${user}:${Date.now()}`)
      username.value = user
      localStorage.setItem('token', token.value)
      localStorage.setItem('username', username.value)
      return true
    }
    return false
  }

  function logout() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return { token, username, isLoggedIn, login, logout }
})
