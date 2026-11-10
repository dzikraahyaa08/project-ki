<template>
  <v-container class="pa-6">
    <v-row>
      <!-- Statistic Cards -->
      <v-col cols="12" sm="4">
        <v-card class="luxury-card pb-2 rounded-xl" elevation="0">
          <v-card-item>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-overline mb-1 text-secondary tracking-widest">Total Produk</div>
                <div class="text-h3 font-weight-black text-primary">
                  <v-progress-circular v-if="loading" indeterminate size="32" color="primary"></v-progress-circular>
                  <span v-else>{{ products.length }}</span>
                </div>
              </div>
              <div class="stat-icon">
                <v-icon size="x-large">mdi-package-variant</v-icon>
              </div>
            </div>
          </v-card-item>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="4">
        <v-card class="luxury-card pb-2 rounded-xl" elevation="0">
          <v-card-item>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-overline mb-1 text-secondary tracking-widest">Total Pengguna</div>
                <div class="text-h3 font-weight-black text-primary">
                  <v-progress-circular v-if="loading" indeterminate size="32" color="primary"></v-progress-circular>
                  <span v-else>{{ users.length }}</span>
                </div>
              </div>
              <div class="stat-icon">
                <v-icon size="x-large">mdi-account-group</v-icon>
              </div>
            </div>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card class="luxury-card pb-2 rounded-xl" elevation="0" to="/admin/audit-logs">
          <v-card-item>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-overline mb-1 text-secondary tracking-widest">Keamanan (A5)</div>
                <div class="text-h4 font-weight-black text-success">
                  Aktif (100%)
                </div>
                <div class="text-caption text-secondary mt-1">Audit Trail & RBAC Siap</div>
              </div>
              <div class="stat-icon text-success">
                <v-icon size="x-large" color="success">mdi-shield-check</v-icon>
              </div>
            </div>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <!-- Product Table -->
    <v-row class="mt-8">
      <v-col cols="12">
        <h3 class="text-primary mb-4 font-weight-bold" style="letter-spacing: 1px">Daftar Produk Terbaru</h3>
        
        <v-card class="rounded-xl luxury-table-card" elevation="0">
          <v-table class="bg-transparent pa-2">
            <thead>
              <tr>
                <th class="text-left text-primary font-weight-bold">ID</th>
                <th class="text-left text-primary font-weight-bold">Nama Barang</th>
                <th class="text-left text-primary font-weight-bold">Merek / Kategori</th>
                <th class="text-left text-primary font-weight-bold">Harga</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="4" class="text-center pa-4">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </td>
              </tr>
              <tr v-else-if="products.length === 0">
                <td colspan="4" class="text-center pa-4 text-secondary">Tidak ada data produk</td>
              </tr>
              <tr v-for="product in products.slice(0, 5)" :key="product.product_id" class="table-row-hover">
                <td class="text-secondary font-weight-medium">#{{ product.product_id }}</td>
                <td class="font-weight-bold text-dark">{{ product.name }}</td>
                <td class="text-secondary">{{ product.brand_name || product.brand_id }}</td>
                <td class="text-primary font-weight-bold">{{ formatPrice(product.price) }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Security Audit Logs Section -->
    <v-row class="mt-6">
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-4">
          <h3 class="text-primary font-weight-bold" style="letter-spacing: 1px">
            <v-icon start color="primary">mdi-shield-alert-outline</v-icon>
            Aktivitas Keamanan Terkini (A5 Accounting & Audit)
          </h3>
          <v-btn color="primary" variant="text" to="/admin/audit-logs" class="text-none font-weight-bold">
            Lihat Semua Log <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
        </div>

        <v-card class="rounded-xl luxury-table-card" elevation="0">
          <v-table class="bg-transparent pa-2">
            <thead>
              <tr>
                <th class="text-left text-primary font-weight-bold">Waktu</th>
                <th class="text-left text-primary font-weight-bold">Aktor</th>
                <th class="text-left text-primary font-weight-bold">Kategori</th>
                <th class="text-left text-primary font-weight-bold">Aksi</th>
                <th class="text-left text-primary font-weight-bold">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in recentLogs" :key="log.id" class="table-row-hover">
                <td class="text-secondary text-caption">{{ log.timestamp }}</td>
                <td class="font-weight-bold text-dark">{{ log.actor }}</td>
                <td><v-chip size="x-small" color="primary" variant="outlined">{{ log.category }}</v-chip></td>
                <td><code>{{ log.action }}</code></td>
                <td>
                  <v-chip size="x-small" :color="log.severity === 'DANGER' ? 'error' : (log.severity === 'WARNING' ? 'warning' : 'success')" variant="tonal" class="font-weight-bold">
                    {{ log.status }}
                  </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'
import { getAuditLogs } from '../services/security'

const products = ref([])
const users = ref([])
const recentLogs = ref([])
const loading = ref(true)

const formatPrice = (price) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price)
}

const fetchData = async () => {
  try {
    const [prodRes, userRes] = await Promise.all([
      apiClient('/products'),
      apiClient('/users')
    ])
    
    if (!prodRes.ok || !userRes.ok) {
      throw new Error('Gagal mengambil data dari server')
    }
    
    const prodData = await prodRes.json()
    const userData = await userRes.json()
    
    // Handle berbagai format response
    products.value = Array.isArray(prodData?.data) ? prodData.data : (Array.isArray(prodData) ? prodData : [])
    users.value = Array.isArray(userData?.data) ? userData.data : (Array.isArray(userData) ? userData : [])
    recentLogs.value = getAuditLogs().slice(0, 5)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.luxury-card {
  background: rgba(255, 255, 255, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  backdrop-filter: blur(20px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04) !important;
  position: relative;
  overflow: hidden;
}

.luxury-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

.luxury-card:hover {
  transform: translateY(-5px) scale(1.02);
  border-color: rgba(184, 134, 11, 0.3) !important;
  box-shadow: 0 15px 45px rgba(184, 134, 11, 0.08) !important;
  background: rgba(255, 255, 255, 0.85) !important;
}

.luxury-table-card {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03) !important;
  transition: all 0.3s ease;
}

.luxury-table-card:hover {
  box-shadow: 0 15px 40px rgba(184, 134, 11, 0.05) !important;
}

.table-row-hover {
  transition: all 0.2s ease;
}

.table-row-hover:hover {
  background-color: rgba(184, 134, 11, 0.04) !important;
}

.stat-icon {
  background: linear-gradient(135deg, #F9F6F0, #F0E6D2);
  border-radius: 16px;
  padding: 16px;
  color: #B8860B;
  box-shadow: 0 4px 15px rgba(184, 134, 11, 0.15), inset 0 2px 0 rgba(255, 255, 255, 0.8);
}

.tracking-widest {
  letter-spacing: 2px;
}

.text-dark {
  color: #2C3E50 !important;
}
</style>
