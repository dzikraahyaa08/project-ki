<template>
  <v-app>
    <v-main class="d-flex align-center justify-center bg-background">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card class="elevation-0 rounded-xl luxury-login-card pb-4">
              <v-card-title class="text-center pt-10 pb-2 text-h4 font-weight-bold luxury-title">
                LUXURY
              </v-card-title>
              <v-card-subtitle class="text-center pb-8 text-secondary font-weight-medium tracking-widest">
                login
              </v-card-subtitle>
              
              <v-card-text class="px-10">
                <v-form @submit.prevent="handleLogin">
                  <v-text-field
                    v-model="loginData.username"
                    label="Username"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    color="primary"
                    class="mb-4"
                    :disabled="loading"
                  ></v-text-field>

                  <v-text-field
                    v-model="loginData.password"
                    label="Password"
                    type="password"
                    prepend-inner-icon="mdi-lock"
                    variant="outlined"
                    color="primary"
                    class="mb-6"
                    :disabled="loading"
                  ></v-text-field>

                  <v-alert
                    v-if="lockoutRemaining > 0"
                    type="error"
                    variant="tonal"
                    density="compact"
                    class="mb-6 rounded-lg font-weight-bold"
                    icon="mdi-shield-alert"
                  >
                    Keamanan Terpicu (A5 Authentication): Terlalu banyak percobaan gagal. Silakan tunggu {{ lockoutRemaining }} detik.
                  </v-alert>

                  <v-alert
                    v-else-if="errorMsg"
                    type="error"
                    variant="tonal"
                    density="compact"
                    class="mb-6 rounded-lg"
                  >
                    {{ errorMsg }}
                  </v-alert>

                  <v-btn
                    type="submit"
                    color="primary"
                    size="x-large"
                    block
                    class="font-weight-bold rounded-lg mt-2 mb-2 text-none"
                    :loading="loading"
                    :disabled="lockoutRemaining > 0 || loading"
                  >
                    {{ lockoutRemaining > 0 ? `Terkunci (${lockoutRemaining}s)` : 'Masuk' }}
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '../services/api'
import {
  checkBruteForceLockout,
  recordFailedLoginAttempt,
  recordSuccessfulLogin
} from '../services/security'

const router = useRouter()
const loading = ref(false)
const errorMsg = ref('')
const lockoutRemaining = ref(0)
let timerInterval = null

const loginData = ref({
  username: '',
  password: ''
})

const checkLockStatus = () => {
  const status = checkBruteForceLockout()
  if (status.isLocked) {
    lockoutRemaining.value = status.remainingSeconds
    startTimer()
  } else {
    lockoutRemaining.value = 0
  }
}

const startTimer = () => {
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    if (lockoutRemaining.value > 0) {
      lockoutRemaining.value--
    } else {
      clearInterval(timerInterval)
      timerInterval = null
      errorMsg.value = ''
    }
  }, 1000)
}

onMounted(() => {
  checkLockStatus()
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

const handleLogin = async () => {
  checkLockStatus()
  if (lockoutRemaining.value > 0) return

  if (!loginData.value.username || !loginData.value.password) {
    errorMsg.value = 'Silakan masukkan username dan password'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const response = await apiClient('/login', {
      method: 'POST',
      body: JSON.stringify(loginData.value)
    })
    
    const data = await response.json()
    
    if (response.ok && data.data?.token) {
      recordSuccessfulLogin(loginData.value.username)
      localStorage.setItem('token', data.data.token)
      // Simpan user_id juga untuk transaksi
      if (data.data?.user?.user_id) {
        localStorage.setItem('user_id', data.data.user.user_id)
      } else if (data.data?.user_id) {
        localStorage.setItem('user_id', data.data.user_id)
      }
      router.push('/admin/dashboard')
    } else if (response.status === 401) {
      const lockRes = recordFailedLoginAttempt(loginData.value.username)
      if (lockRes.isLocked) {
        lockoutRemaining.value = lockRes.remainingSeconds
        startTimer()
      } else {
        errorMsg.value = `Username atau password salah (Percobaan ${lockRes.attempts}/3)`
      }
    } else {
      errorMsg.value = data.message || 'Login gagal. Silakan coba lagi.'
      recordFailedLoginAttempt(loginData.value.username)
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMsg.value = 'Koneksi ke server gagal. Silakan cek koneksi Anda.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.bg-background {
  background-color: #F5F2ED !important;
  background-image: radial-gradient(circle at 50% -20%, #ffffff 0%, transparent 70%);
}

.luxury-login-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.8) !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05) !important;
  transition: box-shadow 0.4s ease, transform 0.4s ease;
  position: relative;
  overflow: hidden;
}

.luxury-login-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

.luxury-login-card:hover {
  box-shadow: 0 20px 45px rgba(184, 134, 11, 0.08) !important;
  transform: translateY(-2px);
}

.luxury-title {
  letter-spacing: 6px;
  background: linear-gradient(45deg, #B8860B, #D4AF37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(184, 134, 11, 0.15);
}

.tracking-widest {
  letter-spacing: 3px;
}
</style>
