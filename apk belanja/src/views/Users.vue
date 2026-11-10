<template>
  <v-container class="pa-6">
    <v-row>
      <v-col cols="12" class="d-flex justify-space-between align-center">
        <h2 class="text-primary font-weight-bold" style="letter-spacing: 1px">Kelola Pengguna</h2>
        <v-btn color="primary" prepend-icon="mdi-plus" @click="openDialog()" elevation="2" class="rounded-lg text-none font-weight-bold">
          Tambah Pengguna
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
                <th class="text-left text-primary font-weight-bold">Username</th>
                <th class="text-left text-primary font-weight-bold">Email</th>
                <th class="text-left text-primary font-weight-bold">Membership</th>
                <th class="text-center text-primary font-weight-bold">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="5" class="text-center pa-4">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </td>
              </tr>
              <tr v-else-if="users.length === 0">
                <td colspan="5" class="text-center pa-4 text-secondary">Tidak ada data pengguna</td>
              </tr>
              <tr v-for="user in users" :key="user.user_id" class="table-row-hover">
                <td class="text-secondary font-weight-bold">#{{ user.user_id }}</td>
                <td class="font-weight-bold text-dark">{{ user.username }}</td>
                <td class="text-secondary">{{ user.email }}</td>
                <td class="text-primary font-weight-bold">{{ user.membership_level }}</td>
                <td class="text-center">
                  <v-btn icon="mdi-pencil" size="small" color="info" variant="tonal" class="mr-2 rounded-lg" @click="openDialog(user)"></v-btn>
                  <v-btn icon="mdi-delete" size="small" color="error" variant="tonal" class="rounded-lg" @click="deleteUser(user.user_id)"></v-btn>
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
          {{ editedId ? 'Edit Pengguna' : 'Tambah Pengguna' }}
        </v-card-title>
        <v-card-text class="px-8 pb-2 mt-4">
          <v-form ref="form" @submit.prevent="saveUser">
            <v-text-field
              v-model="editedItem.username"
              label="Username"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
            <v-text-field
              v-model="editedItem.email"
              label="Email"
              type="email"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-text-field>
            <v-select
              v-model="editedItem.membership_level"
              :items="['Silver', 'Gold', 'Platinum']"
              label="Membership Level"
              variant="outlined"
              color="primary"
              class="mb-4"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions class="px-8 pb-6">
          <v-spacer></v-spacer>
          <v-btn color="secondary" variant="text" @click="dialog = false" class="px-4 text-none font-weight-medium">Batal</v-btn>
          <v-btn color="primary" variant="elevated" @click="saveUser" :loading="saving" class="px-6 font-weight-bold rounded-lg text-none">Simpan</v-btn>
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
import { logSecurityEvent } from '../services/security'

const users = ref([])
const loading = ref(true)

const dialog = ref(false)
const saving = ref(false)
const editedId = ref(null)
const editedItem = ref({
  username: '',
  email: '',
  membership_level: 'Silver'
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const showMessage = (text, color = 'success') => {
  snackbar.value = { show: true, text, color }
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await apiClient('/users')
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }
    const data = await res.json()
    users.value = Array.isArray(data?.data) ? data.data : (Array.isArray(data) ? data : [])
  } catch (error) {
    console.error('Error fetching users:', error)
    showMessage('Gagal mengambil data pengguna', 'error')
  } finally {
    loading.value = false
  }
}

const openDialog = (item = null) => {
  if (item) {
    editedId.value = item.user_id
    editedItem.value = { 
      username: item.username, 
      email: item.email, 
      membership_level: item.membership_level 
    }
  } else {
    editedId.value = null
    editedItem.value = { username: '', email: '', membership_level: 'Silver' }
  }
  dialog.value = true
}

const saveUser = async () => {
  saving.value = true
  const method = editedId.value ? 'PUT' : 'POST'
  const url = editedId.value ? `/users/${editedId.value}` : `/users/register`

  const payload = { ...editedItem.value }

  try {
    const res = await apiClient(url, {
      method,
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      logSecurityEvent({
        action: editedId.value ? 'USER_UPDATE' : 'USER_CREATE',
        category: 'Data Management',
        severity: 'INFO',
        details: `${editedId.value ? 'Mengubah' : 'Menambahkan'} akun pengguna: ${editedItem.value.username} (${editedItem.value.membership_level})`
      })
      showMessage(editedId.value ? 'Pengguna berhasil diupdate' : 'Pengguna berhasil ditambahkan')
      dialog.value = false
      fetchUsers()
    } else {
      const data = await res.json()
      showMessage(data.message || 'Gagal menyimpan pengguna', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  } finally {
    saving.value = false
  }
}

const deleteUser = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus pengguna ini?')) return

  try {
    const res = await apiClient(`/users/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      logSecurityEvent({
        action: 'USER_DELETE',
        category: 'Data Management',
        severity: 'WARNING',
        details: `Menghapus akun pengguna ID #${id}`
      })
      showMessage('Pengguna berhasil dihapus')
      fetchUsers()
    } else {
      showMessage('Gagal menghapus pengguna', 'error')
    }
  } catch (error) {
    showMessage('Terjadi kesalahan', 'error')
  }
}

onMounted(() => {
  fetchUsers()
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
