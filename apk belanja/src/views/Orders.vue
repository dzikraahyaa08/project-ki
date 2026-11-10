<template>
  <v-container class="pa-6">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h2 class="text-primary font-weight-bold" style="letter-spacing: 1px">Kelola Pesanan</h2>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="rounded-xl luxury-table-card" elevation="0">
          <v-table class="bg-transparent pa-2">
            <thead>
              <tr>
                <th class="text-left text-primary font-weight-bold">ID Pesanan</th>
                <th class="text-left text-primary font-weight-bold">ID Pengguna</th>
                <th class="text-left text-primary font-weight-bold">Total Harga</th>
                <th class="text-left text-primary font-weight-bold">Status</th>
                <th class="text-center text-primary font-weight-bold">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="5" class="text-center pa-4">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </td>
              </tr>
              <tr v-else-if="orders.length === 0">
                <td colspan="5" class="text-center pa-4 text-secondary">Tidak ada data pesanan</td>
              </tr>
              <tr v-for="order in orders" :key="order.order_id" class="table-row-hover">
                <td class="text-secondary font-weight-bold">#{{ order.order_id }}</td>
                <td class="font-weight-medium text-dark">{{ order.username || order.user_id || 'N/A' }}</td>
                <td class="text-primary font-weight-bold">{{ formatPrice(order.total_amount) }}</td>
                <td>
                  <v-chip :color="getStatusColor(order.status)" size="small" variant="tonal" class="font-weight-bold">
                    {{ order.status || 'Pending' }}
                  </v-chip>
                </td>
                <td class="text-center">
                  <v-btn icon="mdi-check-circle" size="small" color="success" variant="tonal" class="mr-2 rounded-lg" @click="updateStatus(order.order_id, 'Selesai')" title="Tandai Selesai"></v-btn>
                  <v-btn icon="mdi-delete" size="small" color="error" variant="tonal" class="rounded-lg" @click="deleteOrder(order.order_id)"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'
import { logSecurityEvent } from '../services/security'

const orders = ref([])
const loading = ref(true)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const showMessage = (text, color = 'success') => {
  snackbar.value = { show: true, text, color }
}

const formatPrice = (price) => {
  if (!price) return '-'
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price)
}

const getStatusColor = (status) => {
  if (!status) return 'warning'
  const s = status.toLowerCase()
  if (s.includes('selesai') || s.includes('success') || s.includes('paid')) return 'success'
  if (s.includes('batal') || s.includes('cancel')) return 'error'
  return 'warning'
}

const fetchOrders = async () => {
  loading.value = true
  try {
    const res = await apiClient('/orders')
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }
    const data = await res.json()
    orders.value = Array.isArray(data?.data) ? data.data : (Array.isArray(data) ? data : [])
  } catch (error) {
    console.error('Error fetching orders:', error)
    showMessage('Gagal mengambil data pesanan', 'error')
  } finally {
    loading.value = false
  }
}

const updateStatus = async (id, status) => {
  try {
    const res = await apiClient(`/orders/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ status })
    })
    
    if (res.ok) {
      logSecurityEvent({
        action: 'ORDER_STATUS_UPDATE',
        category: 'Data Management',
        severity: 'INFO',
        details: `Mengubah status pesanan #${id} menjadi "${status}"`
      })
      showMessage('Status pesanan diperbarui')
      fetchOrders()
    } else {
      showMessage('Gagal memperbarui status', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  }
}

const deleteOrder = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus pesanan ini?')) return

  try {
    const res = await apiClient(`/orders/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      logSecurityEvent({
        action: 'ORDER_DELETE',
        category: 'Data Management',
        severity: 'WARNING',
        details: `Menghapus data transaksi pesanan #${id}`
      })
      showMessage('Pesanan berhasil dihapus')
      fetchOrders()
    } else {
      showMessage('Gagal menghapus pesanan', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
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

.text-dark {
  color: #2C3E50 !important;
}
</style>
