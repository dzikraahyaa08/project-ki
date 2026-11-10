<template>
  <v-container class="pa-6">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h2 class="text-primary font-weight-bold" style="letter-spacing: 1px">Kelola Produk</h2>
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openDialog()" elevation="2" class="rounded-lg text-none font-weight-bold">
          Tambah Produk
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="rounded-xl luxury-table-card" elevation="0">
          <v-table class="bg-transparent pa-2">
            <thead>
              <tr>
                <th class="text-left text-primary font-weight-bold">ID</th>
                <th class="text-left text-primary font-weight-bold">Nama Barang</th>
                <th class="text-left text-primary font-weight-bold">Kategori / Merek</th>
                <th class="text-left text-primary font-weight-bold">Harga</th>
                <th class="text-center text-primary font-weight-bold">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="5" class="text-center pa-4">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </td>
              </tr>
              <tr v-else-if="products.length === 0">
                <td colspan="5" class="text-center pa-4 text-secondary">Tidak ada data produk</td>
              </tr>
              <tr v-for="product in products" :key="product.product_id" class="table-row-hover">
                <td class="text-secondary font-weight-bold">#{{ product.product_id }}</td>
                <td class="font-weight-bold text-dark">{{ product.name }}</td>
                <td class="text-secondary">{{ product.brand_name || product.brand_id }}</td>
                <td class="text-primary font-weight-bold">{{ formatPrice(product.price) }}</td>
                <td class="text-center">
                  <v-btn icon="mdi-pencil" size="small" color="info" variant="tonal" class="mr-2 rounded-lg" @click="openDialog(product)"></v-btn>
                  <v-btn icon="mdi-delete" size="small" color="error" variant="tonal" class="rounded-lg" @click="deleteProduct(product.product_id)"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog for Create / Edit -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card class="luxury-dialog rounded-xl" elevation="0">
        <v-card-title class="text-primary font-weight-bold pt-6 px-8" style="letter-spacing: 1px">
          {{ editedId ? 'Edit Produk' : 'Tambah Produk' }}
        </v-card-title>
        <v-card-text class="px-8 pb-2 mt-4">
          <v-form ref="form" @submit.prevent="saveProduct">
            <v-text-field
              v-model="editedItem.name"
              label="Nama Barang"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.brand_id"
              label="ID Merek"
              type="number"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.price"
              label="Harga"
              type="number"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.stock"
              label="Stok"
              type="number"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions class="px-8 pb-6">
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="dialog = false" class="px-4 text-none font-weight-medium">Batal</v-btn>
          <v-btn color="primary" variant="elevated" @click="saveProduct" :loading="saving" class="px-6 font-weight-bold rounded-lg text-none">Simpan</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const products = ref([])
const loading = ref(true)

const dialog = ref(false)
const saving = ref(false)
const editedId = ref(null)
const editedItem = ref({
  name: '',
  brand_id: null,
  price: null,
  stock: null,
  model_year: new Date().getFullYear()
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const showMessage = (text, color = 'success') => {
  snackbar.value = { show: true, text, color }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0
  }).format(price)
}

const fetchProducts = async () => {
  loading.value = true
  try {
    const res = await apiClient('/products')
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }
    const data = await res.json()
    products.value = Array.isArray(data?.data) ? data.data : (Array.isArray(data) ? data : [])
  } catch (error) {
    console.error('Error fetching products:', error)
    showMessage('Gagal mengambil data produk', 'error')
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  if (item) {
    editedId.value = item.product_id
    editedItem.value = { 
      name: item.name, 
      brand_id: item.brand_id, 
      price: item.price, 
      stock: item.stock,
      model_year: item.model_year || new Date().getFullYear()
    }
  } else {
    editedId.value = null
    editedItem.value = { name: '', brand_id: null, price: null, stock: null, model_year: new Date().getFullYear() }
  }
  dialog.value = true
}

const saveProduct = async () => {
  saving.value = true
  const method = editedId.value ? 'PUT' : 'POST'
  const url = editedId.value ? `/products/${editedId.value}` : `/products`

  try {
    const res = await apiClient(url, {
      method,
      body: JSON.stringify(editedItem.value)
    })
    
    if (res.ok) {
      showMessage(editedId.value ? 'Produk berhasil diupdate' : 'Produk berhasil ditambahkan')
      dialog.value = false
      fetchProducts()
    } else {
      const data = await res.json()
      showMessage(data.message || 'Gagal menyimpan produk', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  } finally {
    saving.value = false
  }
}

const deleteProduct = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus produk ini?')) return

  try {
    const res = await apiClient(`/products/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      showMessage('Produk berhasil dihapus')
      fetchProducts()
    } else {
      showMessage('Gagal menghapus produk', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  }
}

onMounted(() => {
  fetchProducts()
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

.luxury-dialog {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1) !important;
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
