import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '../user'
import { describe, it, expect, beforeEach } from 'vitest'

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with no user', () => {
    const store = useUserStore()
    expect(store.user).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })

  it('logs in user', async () => {
    const store = useUserStore()
    await store.login({ username: 'test', password: 'password' })
    expect(store.user).not.toBeNull()
    expect(store.isLoggedIn).toBe(true)
    expect(store.user?.username).toBe('test')
  })

  it('logs out user', async () => {
    const store = useUserStore()
    await store.login({ username: 'test', password: 'password' })
    store.logout()
    expect(store.user).toBeNull()
    expect(store.isLoggedIn).toBe(false)
  })
})
