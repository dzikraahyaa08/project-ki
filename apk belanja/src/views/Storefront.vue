<template>
  <v-app class="bg-background">
    <v-app-bar color="background" elevation="4" class="border-b-gold">
      <v-container class="d-flex align-center py-0">
        <h2 class="text-primary font-weight-bold tracking-widest" style="cursor: pointer" @click="scrollTo('home')">LUXURY STORE</h2>
        <v-spacer></v-spacer>
        <v-btn variant="text" class="text-secondary hover-gold" @click="scrollTo('home')">Home</v-btn>
        <v-btn variant="text" class="text-secondary hover-gold" @click="scrollToProducts">Koleksi</v-btn>
        <v-btn variant="text" class="text-secondary hover-gold" @click="scrollTo('about')">Tentang Kami</v-btn>
        
        <!-- Customer Session Buttons -->
        <template v-if="customerSession">
          <v-menu offset-y>
            <template v-slot:activator="{ props }">
              <v-btn variant="outlined" color="primary" class="hover-gold ml-2" v-bind="props" prepend-icon="mdi-account-circle">
                {{ customerSession.username }}
              </v-btn>
            </template>
            <v-list class="border-gold mt-1 bg-white">
              <v-list-item @click="openHistory" prepend-icon="mdi-receipt-clock" class="text-secondary hover-gold">
                <v-list-item-title>Riwayat Belanja</v-list-item-title>
              </v-list-item>
              <v-list-item @click="logoutCustomer" prepend-icon="mdi-logout" class="text-error">
                <v-list-item-title>Keluar</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
        <template v-else>
          <v-btn variant="text" class="text-secondary hover-gold ml-2" prepend-icon="mdi-login" @click="customerAuthDialog = true">
            Masuk / Daftar
          </v-btn>
        </template>

        <v-btn icon color="primary" class="ml-4" @click="cartDrawer = !cartDrawer">
          <v-badge :content="cart.length" :model-value="cart.length > 0" color="error">
            <v-icon>mdi-cart</v-icon>
          </v-badge>
        </v-btn>
        <v-btn variant="outlined" color="primary" class="ml-4" to="/login">Admin</v-btn>
      </v-container>
    </v-app-bar>

    <!-- Cart Navigation Drawer -->
    <v-navigation-drawer v-model="cartDrawer" location="right" temporary width="400" color="background">
      <div class="d-flex align-center pa-4 border-b-gold">
        <h3 class="text-h6 text-primary font-weight-bold mb-0">Keranjang Belanja</h3>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-close" variant="text" color="grey" @click="cartDrawer = false"></v-btn>
      </div>

      <v-container v-if="cart.length === 0" class="text-center py-12">
        <v-icon size="64" color="grey-darken-2" class="mb-4">mdi-cart-outline</v-icon>
        <p class="text-grey">Keranjang belanja Anda masih kosong.</p>
        <v-btn color="primary" class="mt-4" @click="cartDrawer = false; scrollToProducts()">Mulai Belanja</v-btn>
      </v-container>

      <v-list v-else bg-color="transparent" class="pa-4">
        <v-list-item v-for="(item, index) in cart" :key="index" class="mb-4 bg-white rounded-lg border-gold pa-3">
          <template v-slot:prepend>
            <div class="cart-item-img bg-grey-lighten-3 d-flex align-center justify-center rounded mr-4">
              <v-icon color="grey">mdi-package-variant</v-icon>
            </div>
          </template>
          
          <v-list-item-title class="font-weight-bold text-black mb-1">{{ item.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-primary">{{ formatPrice(item.price) }}</v-list-item-subtitle>
          
          <template v-slot:append>
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeFromCart(index)"></v-btn>
          </template>
        </v-list-item>
      </v-list>

      <template v-slot:append v-if="cart.length > 0">
        <div class="pa-4 border-t-gold bg-background">
          <div class="d-flex justify-space-between mb-4">
            <span class="text-grey">Total:</span>
            <span class="text-h6 text-primary font-weight-bold">{{ formatPrice(cartTotal) }}</span>
          </div>
          <v-btn block color="primary" size="x-large" class="font-weight-bold rounded-lg" @click="openCheckout">
            CHECKOUT SEKARANG
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- Checkout Dialog -->
    <v-dialog v-model="checkoutDialog" max-width="600">
      <v-card color="background" class="border-gold">
        <v-card-title class="text-h5 text-primary pa-6 pb-2 border-b-gold font-weight-bold">
          Selesaikan Pembelian
        </v-card-title>
        
        <v-card-text class="pa-6">
          <h4 class="text-black mb-4">Informasi Pengiriman</h4>
          <v-form ref="checkoutForm" v-model="isCheckoutValid">
            <v-text-field
              v-model="checkoutData.nama"
              label="Nama Lengkap"
              variant="outlined"
              color="primary"
              :rules="[v => !!v || 'Nama diperlukan']"
              class="mb-2"
            ></v-text-field>
            
            <v-text-field
              v-model="checkoutData.telepon"
              label="Nomor Telepon"
              variant="outlined"
              color="primary"
              :rules="[v => !!v || 'Nomor telepon diperlukan']"
              class="mb-2"
            ></v-text-field>
            
            <v-textarea
              v-model="checkoutData.alamat"
              label="Alamat Lengkap"
              variant="outlined"
              color="primary"
              rows="3"
              :rules="[v => !!v || 'Alamat diperlukan']"
              class="mb-4"
            ></v-textarea>
          </v-form>

          <v-divider class="mb-4 border-gold"></v-divider>
          
          <div class="d-flex justify-space-between mb-2">
            <span class="text-grey">Subtotal ({{ cart.length }} produk)</span>
            <span class="text-black">{{ formatPrice(cartTotal) }}</span>
          </div>
          <div class="d-flex justify-space-between mb-4">
            <span class="text-grey">Biaya Pengiriman</span>
            <span class="text-black">Gratis</span>
          </div>
          <div class="d-flex justify-space-between align-center">
            <span class="text-h6 text-black">Total Pembayaran</span>
            <span class="text-h5 text-primary font-weight-bold">{{ formatPrice(cartTotal) }}</span>
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-6 pt-0">
          <v-spacer></v-spacer>
          <v-btn variant="text" color="grey" @click="checkoutDialog = false">Batal</v-btn>
          <v-btn 
            color="primary" 
            variant="elevated" 
            class="px-6 font-weight-bold" 
            :disabled="!isCheckoutValid"
            :loading="isProcessing"
            @click="processCheckout"
          >
            BAYAR SEKARANG
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-main id="home">
      <!-- Hero Section -->
      <section class="hero-section d-flex align-center justify-center">
        <div class="text-center px-4">
          <h1 class="text-h2 text-sm-h1 font-weight-bold text-white mb-4">
            ELEVATE YOUR <span class="text-primary">STYLE</span>
          </h1>
          <p class="text-h6 text-grey-lighten-1 mb-8 max-w-md mx-auto">
            Temukan koleksi barang mewah eksklusif dari brand ternama dunia dengan kualitas terbaik.
          </p>
          <v-btn size="x-large" color="primary" class="font-weight-bold px-8 rounded-pill" @click="scrollToProducts">
            LIHAT KOLEKSI
          </v-btn>
        </div>
      </section>

      <!-- Products Section -->
      <section id="products" class="py-16">
        <v-container>
          <div class="text-center mb-12">
            <h2 class="text-h4 text-primary font-weight-bold mb-2">Koleksi Terbaru</h2>
            <div class="gold-divider mx-auto"></div>
          </div>

          <v-row v-if="loading">
            <v-col cols="12" class="text-center py-12">
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            </v-col>
          </v-row>
          
          <v-row v-else-if="products.length === 0">
            <v-col cols="12" class="text-center text-grey py-12">
              Belum ada produk yang tersedia saat ini.
            </v-col>
          </v-row>

          <v-row v-else>
            <v-col cols="12" sm="6" md="4" lg="3" v-for="product in products" :key="product.product_id">
              <v-card class="product-card bg-white rounded-xl border-gold h-100 d-flex flex-column" elevation="8">
                <!-- Image Placeholder -->
                <div class="product-image-container bg-background d-flex align-center justify-center">
                  <v-icon size="64" color="grey-darken-2">mdi-package-variant-closed</v-icon>
                </div>
                
                <v-card-text class="flex-grow-1 px-5 pt-5 pb-2">
                  <div class="text-caption text-primary mb-1 text-uppercase tracking-widest">{{ product.brand_name || product.brand_id }}</div>
                  <h3 class="text-h6 font-weight-bold text-grey-darken-4 mb-2 text-truncate" :title="product.name">
                    {{ product.name }}
                  </h3>
                  <div class="text-h6 text-primary font-weight-medium">
                    {{ formatPrice(product.price) }}
                  </div>
                </v-card-text>
                
                <v-card-actions class="px-5 pb-5 pt-0">
                  <v-btn block color="primary" variant="elevated" class="rounded-lg font-weight-bold" @click="addToCart(product)">
                    BELI SEKARANG
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </section>

      <!-- About Section -->
      <section id="about" class="py-16 bg-background border-t-gold">
        <v-container>
          <v-row align="center">
            <v-col cols="12" md="6">
              <div class="about-image-placeholder bg-white border-gold rounded-xl d-flex align-center justify-center">
                <v-icon size="80" color="primary">mdi-storefront-outline</v-icon>
              </div>
            </v-col>
            <v-col cols="12" md="6" class="pl-md-8 mt-8 mt-md-0">
              <h2 class="text-h4 text-primary font-weight-bold mb-4">Tentang Kami</h2>
              <div class="gold-divider mb-6"></div>
              <p class="text-body-1 text-grey-darken-3 mb-4">
                Luxury Store adalah destinasi utama untuk menemukan barang-barang mewah eksklusif. Kami menyediakan platform jual beli produk berkualitas tinggi dari brand-brand ternama di seluruh dunia.
              </p>
              <p class="text-body-1 text-grey-darken-3 mb-6">
                Dengan komitmen terhadap keaslian dan kualitas, setiap produk yang dijual di platform kami telah melewati proses kurasi yang ketat untuk memastikan kepuasan pelanggan.
              </p>
              <v-btn variant="outlined" color="primary" class="px-8 rounded-pill font-weight-bold">
                PELAJARI LEBIH LANJUT
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </section>
    </v-main>

    <!-- Footer -->
    <v-footer color="background" class="border-t-gold py-8">
      <v-container class="text-center">
        <h3 class="text-primary font-weight-bold mb-4 tracking-widest">LUXURY STORE</h3>
        <p class="text-grey-darken-3 text-body-2">
          &copy; {{ new Date().getFullYear() }} Luxury Store. All rights reserved.
        </p>
      </v-container>
    </v-footer>

    <!-- Customer Auth Dialog (Login/Register) -->
    <v-dialog v-model="customerAuthDialog" max-width="500">
      <v-card color="white" class="border-gold rounded-xl">
        <v-tabs v-model="activeTab" align-tabs="center" color="primary" bg-color="background">
          <v-tab value="login">Masuk</v-tab>
          <v-tab value="register">Daftar</v-tab>
        </v-tabs>

        <v-window v-model="activeTab" class="pa-6">
          <!-- Login Tab -->
          <v-window-item value="login">
            <h3 class="text-h6 text-black mb-4 text-center font-weight-bold">Masuk ke Akun Anda</h3>
            <v-form ref="customerLoginForm" v-model="isLoginFormValid" @submit.prevent="handleCustomerLogin">
              <v-text-field
                v-model="customerLoginData.email_or_username"
                label="Username atau Email"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-account-outline"
                :rules="[v => !!v || 'Username atau Email diperlukan']"
                class="mb-4"
              ></v-text-field>
              
              <v-btn
                type="submit"
                block
                color="primary"
                size="large"
                class="font-weight-bold rounded-lg"
                :loading="authLoading"
                :disabled="!isLoginFormValid"
              >
                MASUK
              </v-btn>
            </v-form>
          </v-window-item>

          <!-- Register Tab -->
          <v-window-item value="register">
            <h3 class="text-h6 text-black mb-4 text-center font-weight-bold">Daftar Akun Baru</h3>
            <v-form ref="customerRegisterForm" v-model="isRegisterFormValid" @submit.prevent="handleCustomerRegister">
              <v-text-field
                v-model="customerRegisterData.username"
                label="Username"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-account-outline"
                :rules="[v => !!v || 'Username diperlukan']"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="customerRegisterData.email"
                label="Email"
                type="email"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-email-outline"
                :rules="[
                  v => !!v || 'Email diperlukan',
                  v => /.+@.+\..+/.test(v) || 'Format email tidak valid'
                ]"
                class="mb-4"
              ></v-text-field>

              <v-select
                v-model="customerRegisterData.membership_level"
                label="Level Membership"
                :items="['Silver', 'Gold', 'Platinum']"
                variant="outlined"
                color="primary"
                prepend-inner-icon="mdi-crown-outline"
                class="mb-6"
              ></v-select>

              <v-btn
                type="submit"
                block
                color="primary"
                size="large"
                class="font-weight-bold rounded-lg"
                :loading="authLoading"
                :disabled="!isRegisterFormValid"
              >
                DAFTAR
              </v-btn>
            </v-form>
          </v-window-item>
        </v-window>
      </v-card>
    </v-dialog>

    <!-- Shopping History Dialog -->
    <v-dialog v-model="historyDialog" max-width="800">
      <v-card color="white" class="border-gold rounded-xl">
        <v-card-title class="text-h5 text-primary pa-6 pb-2 border-b-gold font-weight-bold d-flex align-center">
          <v-icon color="primary" class="mr-2">mdi-receipt-clock</v-icon>
          Riwayat Belanja Anda
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" color="grey" @click="historyDialog = false"></v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <div v-if="historyLoading" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
            <p class="text-grey mt-4">Memuat riwayat belanja...</p>
          </div>

          <div v-else-if="historyOrders.length === 0" class="text-center py-12">
            <v-icon size="64" color="grey-darken-2" class="mb-4">mdi-clipboard-text-search-outline</v-icon>
            <p class="text-grey">Anda belum memiliki riwayat pembelian.</p>
            <v-btn color="primary" class="mt-4" @click="historyDialog = false; scrollToProducts()">Belanja Sekarang</v-btn>
          </div>

          <div v-else>
            <v-table theme="light" bg-color="transparent" class="history-table">
              <thead>
                <tr>
                  <th class="text-left text-primary font-weight-bold">ID Transaksi</th>
                  <th class="text-left text-primary font-weight-bold">Tanggal</th>
                  <th class="text-left text-primary font-weight-bold">Total Pembayaran</th>
                  <th class="text-left text-primary font-weight-bold">Status</th>
                  <th class="text-center text-primary font-weight-bold">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in historyOrders" :key="order.order_id">
                  <td class="font-weight-bold text-black">#{{ order.order_id }}</td>
                  <td class="text-grey">{{ formatDate(order.order_date) }}</td>
                  <td class="text-black">{{ formatPrice(order.total_amount) }}</td>
                  <td>
                    <v-chip
                      :color="getStatusColor(order.status)"
                      text-color="white"
                      size="small"
                      class="font-weight-bold"
                    >
                      {{ order.status }}
                    </v-chip>
                  </td>
                  <td class="text-center">
                    <v-btn
                      color="primary"
                      variant="outlined"
                      size="small"
                      prepend-icon="mdi-eye"
                      @click="showOrderDetail(order.order_id)"
                    >
                      Detail
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Order Detail Dialog -->
    <v-dialog v-model="detailDialog" max-width="600">
      <v-card color="white" class="border-gold rounded-xl">
        <v-card-title class="text-h5 text-primary pa-6 pb-2 border-b-gold font-weight-bold d-flex align-center">
          Detail Transaksi #{{ orderDetail?.order_id }}
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" color="grey" @click="detailDialog = false"></v-btn>
        </v-card-title>

        <v-card-text class="pa-6">
          <div v-if="detailLoading" class="text-center py-8">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
          </div>

          <div v-else-if="orderDetail">
            <div class="mb-6">
              <div class="d-flex justify-space-between mb-2">
                <span class="text-grey">Tanggal Transaksi:</span>
                <span class="text-black font-weight-bold">{{ formatDate(orderDetail.order_date) }}</span>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-grey">Status Pesanan:</span>
                <v-chip :color="getStatusColor(orderDetail.status)" size="small" class="font-weight-bold">
                  {{ orderDetail.status }}
                </v-chip>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-grey">Total Belanja:</span>
                <span class="text-primary font-weight-bold text-h6">{{ formatPrice(orderDetail.total_amount) }}</span>
              </div>
            </div>

            <v-divider class="mb-4 border-gold"></v-divider>

            <h4 class="text-black mb-3 font-weight-bold">Daftar Produk</h4>
            <v-list bg-color="transparent" class="pa-0">
              <v-list-item
                v-for="(item, idx) in orderDetail.items"
                :key="idx"
                class="px-0 py-3 border-b-gold-subtle"
              >
                <div class="d-flex w-100 justify-space-between align-center">
                  <div>
                    <div class="font-weight-bold text-black">{{ item.name }}</div>
                    <div class="text-caption text-primary text-uppercase">{{ item.brand_name }}</div>
                    <div class="text-grey text-caption">{{ item.quantity }} x {{ formatPrice(item.price) }}</div>
                  </div>
                  <div class="text-black font-weight-bold">
                    {{ formatPrice(item.subtotal) }}
                  </div>
                </div>
              </v-list-item>
            </v-list>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '../services/api'

const products = ref([])
const loading = ref(true)

const router = useRouter()

// Customer Session State
const customerSession = ref(null)
const customerAuthDialog = ref(false)
const historyDialog = ref(false)
const detailDialog = ref(false)
const activeTab = ref('login')
const authLoading = ref(false)
const historyLoading = ref(false)
const detailLoading = ref(false)

const isLoginFormValid = ref(false)
const isRegisterFormValid = ref(false)

const customerLoginData = ref({
  email_or_username: ''
})

const customerRegisterData = ref({
  username: '',
  email: '',
  membership_level: 'Silver'
})

const historyOrders = ref([])
const orderDetail = ref(null)

// Cart State
const cart = ref([])
const cartDrawer = ref(false)

// Checkout State
const checkoutDialog = ref(false)
const isCheckoutValid = ref(false)
const isProcessing = ref(false)
const checkoutData = ref({
  nama: '',
  telepon: '',
  alamat: ''
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusColor = (status) => {
  if (!status) return 'grey'
  const s = status.toLowerCase()
  if (s === 'pending') return 'warning'
  if (s === 'completed' || s === 'selesai' || s === 'success') return 'success'
  if (s === 'canceled' || s === 'batal') return 'error'
  return 'primary'
}

const cartTotal = computed(() => {
  return cart.value.reduce((total, item) => total + Number(item.price), 0)
})

const addToCart = (product) => {
  cart.value.push(product)
  cartDrawer.value = true
}

const removeFromCart = (index) => {
  cart.value.splice(index, 1)
}

const openCheckout = () => {
  if (cart.value.length === 0) {
    alert('Keranjang belanja Anda kosong. Silakan tambahkan produk terlebih dahulu.')
    return
  }
  cartDrawer.value = false
  
  // Periksa apakah customer sudah login
  if (!customerSession.value) {
    alert('Silakan masuk atau daftar akun terlebih dahulu untuk menyelesaikan pembelian dan mencatat riwayat belanja Anda.')
    activeTab.value = 'login'
    customerAuthDialog.value = true
    return
  }
  
  // Isi nama otomatis dari session
  checkoutData.value.nama = customerSession.value.username
  checkoutDialog.value = true
}

const handleCustomerLogin = async () => {
  if (!customerLoginData.value.email_or_username) return
  
  authLoading.value = true
  try {
    const res = await apiClient('/customer/login', {
      method: 'POST',
      body: JSON.stringify(customerLoginData.value),
      skipAuthRedirect: true
    })
    const data = await res.json()
    if (res.ok && data.data) {
      const user = data.data
      customerSession.value = user
      localStorage.setItem('customer', JSON.stringify(user))
      customerAuthDialog.value = false
      customerLoginData.value.email_or_username = ''
      alert(`Selamat datang kembali, ${user.username}!`)
      
      if (cart.value.length > 0) {
        checkoutData.value.nama = user.username
        checkoutDialog.value = true
      }
    } else {
      alert(data.meta?.message || data.message || 'Login gagal. Akun tidak ditemukan.')
    }
  } catch (error) {
    console.error('Customer login error:', error)
    alert('Terjadi kesalahan koneksi saat login.')
  } finally {
    authLoading.value = false
  }
}

const handleCustomerRegister = async () => {
  if (!customerRegisterData.value.username || !customerRegisterData.value.email) return

  authLoading.value = true
  try {
    const res = await apiClient('/customer/register', {
      method: 'POST',
      body: JSON.stringify(customerRegisterData.value),
      skipAuthRedirect: true
    })
    const data = await res.json()
    if (res.ok && data.data) {
      const user = data.data
      customerSession.value = user
      localStorage.setItem('customer', JSON.stringify(user))
      customerAuthDialog.value = false
      customerRegisterData.value = { username: '', email: '', membership_level: 'Silver' }
      alert(`Registrasi berhasil! Selamat datang, ${user.username}!`)

      if (cart.value.length > 0) {
        checkoutData.value.nama = user.username
        checkoutDialog.value = true
      }
    } else {
      alert(data.meta?.message || data.message || 'Registrasi gagal. Username/email mungkin sudah terdaftar.')
    }
  } catch (error) {
    console.error('Customer register error:', error)
    alert('Terjadi kesalahan koneksi saat registrasi.')
  } finally {
    authLoading.value = false
  }
}

const logoutCustomer = () => {
  customerSession.value = null
  localStorage.removeItem('customer')
  alert('Anda telah keluar dari akun customer.')
}

const openHistory = async () => {
  if (!customerSession.value) {
    activeTab.value = 'login'
    customerAuthDialog.value = true
    return
  }

  historyOrders.value = []
  historyDialog.value = true
  historyLoading.value = true
  try {
    const res = await apiClient(`/customer/orders/${customerSession.value.user_id}`, { skipAuthRedirect: true })
    const data = await res.json()
    if (res.ok && data.data) {
      historyOrders.value = data.data
    } else {
      console.error('Failed to fetch history:', data)
    }
  } catch (error) {
    console.error('Error fetching history:', error)
  } finally {
    historyLoading.value = false
  }
}

const showOrderDetail = async (orderId) => {
  orderDetail.value = null
  detailDialog.value = true
  detailLoading.value = true
  try {
    const res = await apiClient(`/customer/orders/detail/${orderId}`, { skipAuthRedirect: true })
    const data = await res.json()
    if (res.ok && data.data) {
      orderDetail.value = data.data
    } else {
      console.error('Failed to fetch order detail:', data)
    }
  } catch (error) {
    console.error('Error fetching order detail:', error)
  } finally {
    detailLoading.value = false
  }
}

const processCheckout = async () => {
  // Validasi cart
  if (cart.value.length === 0) {
    alert('Keranjang belanja kosong. Silakan tambahkan produk terlebih dahulu.')
    return
  }

  // Validasi form
  if (!checkoutData.value.nama || !checkoutData.value.telepon || !checkoutData.value.alamat) {
    alert('Silakan lengkapi semua data pengiriman (Nama, Nomor Telepon, Alamat)')
    return
  }

  if (!customerSession.value) {
    alert('Silakan login terlebih dahulu.')
    return
  }
  
  isProcessing.value = true
  
  try {
    // Build order items array dari cart
    const orderItems = cart.value.map(item => ({
      product_id: item.product_id,
      quantity: 1,
      price: item.price
    }))

    const payload = {
      user_id: customerSession.value.user_id,
      items: orderItems
    }
    
    console.log('Sending customer order payload:', payload)
    
    const res = await apiClient('/customer/orders', {
      method: 'POST',
      body: JSON.stringify(payload),
      skipAuthRedirect: true
    })
    
    const responseData = await res.json()
    console.log('Customer order response:', res.status, responseData)
    
    if (res.ok) {
      checkoutDialog.value = false
      cart.value = []
      checkoutData.value = { nama: '', telepon: '', alamat: '' }
      alert('✅ Pesanan berhasil dibuat!\n\nPesanan Anda telah dicatat dalam riwayat belanja.')
    } else if (res.status === 400) {
      alert('❌ Validasi Error:\n' + (responseData.meta?.message || responseData.message || JSON.stringify(responseData)))
    } else {
      alert('❌ Gagal membuat pesanan:\n' + (responseData.meta?.message || responseData.message || 'Terjadi kesalahan pada server. Coba lagi nanti.'))
    }
  } catch (error) {
    console.error('Checkout error:', error)
    alert('❌ Kesalahan Jaringan:\nTidak dapat terhubung ke server. Periksa koneksi internet Anda.')
  } finally {
    isProcessing.value = false
  }
}

const scrollTo = (id) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const scrollToProducts = () => {
  scrollTo('products')
}

const fetchProducts = async () => {
  loading.value = true

  // Fallback sample products to show if API requires authentication
  const sampleProducts = [
    { product_id: 'sample-1', name: 'Jaket Kulit Premium', brand_name: 'Maison Luxe', price: 2500000 },
    { product_id: 'sample-2', name: 'Sepatu Formal Classic', brand_name: 'Elegance Co.', price: 1750000 },
    { product_id: 'sample-3', name: 'Tas Tangan Eksklusif', brand_name: 'Aurora', price: 3200000 },
    { product_id: 'sample-4', name: 'Kemeja Sutra', brand_name: 'Silken', price: 950000 }
  ]

  try {
    const res = await apiClient('/products', { skipAuthRedirect: true })

    if (res.status === 401) {
      // Backend requires authentication — use local sample data so storefront still shows collections
      console.info('Produk memerlukan autentikasi, menampilkan produk contoh.')
      products.value = sampleProducts
    } else if (!res.ok) {
      console.warn(`Failed to fetch products: ${res.status} ${res.statusText}`)
      products.value = sampleProducts
    } else {
      const data = await res.json()
      const parsedData = Array.isArray(data?.data) ? data.data : (Array.isArray(data) ? data : [])
      products.value = parsedData.length > 0 ? parsedData : sampleProducts
    }
  } catch (error) {
    console.error('Error fetching products:', error)
    products.value = sampleProducts
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProducts()
  
  const storedCustomer = localStorage.getItem('customer')
  if (storedCustomer) {
    try {
      customerSession.value = JSON.parse(storedCustomer)
    } catch (e) {
      console.error(e)
    }
  }
})
</script>

<style scoped>
.border-b-gold {
  border-bottom: 1px solid rgba(255, 215, 0, 0.2) !important;
}
.border-t-gold {
  border-top: 1px solid rgba(255, 215, 0, 0.2) !important;
}
.border-gold {
  border: 1px solid rgba(255, 215, 0, 0.2);
  transition: all 0.3s ease;
}
.tracking-widest {
  letter-spacing: 0.1em;
}
.hover-gold:hover {
  color: #FFD700 !important;
}

.hero-section {
  min-height: 70vh;
  background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)), 
              url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2070&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
}

.gold-divider {
  height: 3px;
  width: 60px;
  background-color: #FFD700;
  border-radius: 2px;
}

.product-image-container {
  height: 250px;
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
}

.cart-item-img {
  width: 50px;
  height: 50px;
}

.about-image-placeholder {
  height: 400px;
  width: 100%;
}

.product-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.15) !important;
  border-color: rgba(255, 215, 0, 0.5);
}

.border-b-gold-subtle {
  border-bottom: 1px solid rgba(255, 215, 0, 0.1) !important;
}

.history-table th {
  border-bottom: 2px solid rgba(255, 215, 0, 0.2) !important;
}

.history-table td {
  border-bottom: 1px solid rgba(255, 215, 0, 0.1) !important;
}
</style>
