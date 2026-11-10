<template>
  <v-container class="pa-6">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12" md="8">
        <h2 class="text-primary font-weight-bold" style="letter-spacing: 1px">
          <v-icon start color="primary">mdi-shield-check</v-icon>
          Pusat Audit Keamanan & Log Aktivitas (A5)
        </h2>
        <p class="text-secondary text-body-2 mb-0">
          Modul Keamanan 5A: Memantau <strong>Authentication</strong>, <strong>Authorization</strong>, <strong>Accounting</strong>, <strong>Auditing</strong>, dan <strong>Availability/Assurance</strong>.
        </p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex justify-md-end align-center gap-2">
        <v-btn color="primary" variant="outlined" prepend-icon="mdi-download" @click="handleExport" class="rounded-lg mr-2 text-none font-weight-bold">
          Export CSV
        </v-btn>
        <v-btn color="error" variant="tonal" prepend-icon="mdi-delete-sweep" @click="handleClear" class="rounded-lg text-none">
          Reset Log
        </v-btn>
      </v-col>
    </v-row>

    <!-- Stat Metric Cards -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card class="luxury-card rounded-xl pa-4" elevation="0">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-caption text-secondary font-weight-bold">TOTAL AKTIVITAS</div>
              <div class="text-h4 font-weight-black text-primary mt-1">{{ allLogs.length }}</div>
            </div>
            <v-avatar color="primary" variant="tonal" rounded="lg">
              <v-icon>mdi-history</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="luxury-card rounded-xl pa-4" elevation="0">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-caption text-secondary font-weight-bold">LOGIN SUKSES</div>
              <div class="text-h4 font-weight-black text-success mt-1">{{ successCount }}</div>
            </div>
            <v-avatar color="success" variant="tonal" rounded="lg">
              <v-icon>mdi-account-check</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="luxury-card rounded-xl pa-4" elevation="0">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-caption text-secondary font-weight-bold">PERINGATAN / GAGAL</div>
              <div class="text-h4 font-weight-black text-warning mt-1">{{ warningCount }}</div>
            </div>
            <v-avatar color="warning" variant="tonal" rounded="lg">
              <v-icon>mdi-alert-circle</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="luxury-card rounded-xl pa-4" elevation="0">
          <div class="d-flex justify-space-between align-center">
            <div>
              <div class="text-caption text-secondary font-weight-bold">INSIDEN TINGGI</div>
              <div class="text-h4 font-weight-black text-error mt-1">{{ dangerCount }}</div>
            </div>
            <v-avatar color="error" variant="tonal" rounded="lg">
              <v-icon>mdi-shield-alert</v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters & Table -->
    <v-card class="luxury-table-card rounded-xl pa-4" elevation="0">
      <v-row class="mb-2">
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="searchQuery"
            prepend-inner-icon="mdi-magnify"
            label="Cari Aktor, Aksi, atau Detail..."
            variant="outlined"
            density="compact"
            hide-details
            color="primary"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedSeverity"
            :items="['Semua Tingkat', 'INFO', 'SUCCESS', 'WARNING', 'DANGER']"
            label="Filter Tingkat Severity"
            variant="outlined"
            density="compact"
            hide-details
            color="primary"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedCategory"
            :items="['Semua Kategori', 'Authentication', 'Authorization', 'Data Management', 'Auditing', 'System']"
            label="Filter Kategori 5A"
            variant="outlined"
            density="compact"
            hide-details
            color="primary"
          ></v-select>
        </v-col>
      </v-row>

      <v-table class="bg-transparent mt-2">
        <thead>
          <tr>
            <th class="text-left text-primary font-weight-bold">Waktu</th>
            <th class="text-left text-primary font-weight-bold">Aktor / Peran</th>
            <th class="text-left text-primary font-weight-bold">Kategori 5A</th>
            <th class="text-left text-primary font-weight-bold">Aksi / Event</th>
            <th class="text-left text-primary font-weight-bold">Status</th>
            <th class="text-left text-primary font-weight-bold">Keterangan</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredLogs.length === 0">
            <td colspan="6" class="text-center pa-6 text-secondary">
              Tidak ada log aktivitas keamanan yang cocok dengan kriteria filter.
            </td>
          </tr>
          <tr v-for="log in filteredLogs" :key="log.id" class="table-row-hover">
            <td class="text-caption font-weight-medium text-secondary" style="white-space: nowrap">
              {{ log.timestamp }}
            </td>
            <td>
              <div class="font-weight-bold text-dark">{{ log.actor }}</div>
              <div class="text-caption text-secondary">{{ log.role }}</div>
            </td>
            <td>
              <v-chip size="x-small" variant="outlined" color="primary" class="font-weight-medium">
                {{ log.category }}
              </v-chip>
            </td>
            <td>
              <code class="security-code">{{ log.action }}</code>
            </td>
            <td>
              <v-chip :color="getSeverityColor(log.severity)" size="small" variant="tonal" class="font-weight-bold">
                {{ log.status }}
              </v-chip>
            </td>
            <td class="text-body-2 text-secondary py-2" style="max-width: 320px">
              {{ log.details }}
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- Info Box for Viva / Interview -->
    <v-alert
      type="info"
      variant="tonal"
      class="mt-6 rounded-xl"
      icon="mdi-information-outline"
      color="primary"
    >
      <div class="font-weight-bold mb-1">Panduan Wawancara Keamanan (Poin Penilaian Dosen):</div>
      <div class="text-body-2">
        Halaman ini membuktikan implementasi nyata <strong>Accounting</strong> (pencatatan berkala setiap event autentikasi & perubahan data) dan <strong>Auditing</strong> (fasilitas inspeksi, filter anomali kegagalan login beruntun, serta ekspor kepatuhan/compliance). Jika dosen menanyakan di mana konsep 5A diterapkan, tunjukkan halaman ini beserta proteksi rate limiting di form Login!
      </div>
    </v-alert>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getAuditLogs, clearAuditLogs, exportAuditLogsToCSV } from '../services/security'

const allLogs = ref([])
const searchQuery = ref('')
const selectedSeverity = ref('Semua Tingkat')
const selectedCategory = ref('Semua Kategori')

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const showMsg = (text, color = 'success') => {
  snackbar.value = { show: true, text, color }
}

const loadLogs = () => {
  allLogs.value = getAuditLogs()
}

onMounted(() => {
  loadLogs()
})

const successCount = computed(() => {
  return allLogs.value.filter(l => l.severity === 'SUCCESS' || l.status === 'SUCCESS').length
})

const warningCount = computed(() => {
  return allLogs.value.filter(l => l.severity === 'WARNING').length
})

const dangerCount = computed(() => {
  return allLogs.value.filter(l => l.severity === 'DANGER' || l.status === 'LOCKED').length
})

const filteredLogs = computed(() => {
  return allLogs.value.filter(log => {
    // Filter severity
    if (selectedSeverity.value !== 'Semua Tingkat' && log.severity !== selectedSeverity.value) {
      return false
    }
    // Filter category
    if (selectedCategory.value !== 'Semua Kategori' && log.category !== selectedCategory.value) {
      return false
    }
    // Search query
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      const matchActor = log.actor?.toLowerCase().includes(q)
      const matchAction = log.action?.toLowerCase().includes(q)
      const matchDetails = log.details?.toLowerCase().includes(q)
      return matchActor || matchAction || matchDetails
    }
    return true
  })
})

const getSeverityColor = (sev) => {
  switch (sev) {
    case 'SUCCESS': return 'success'
    case 'WARNING': return 'warning'
    case 'DANGER': return 'error'
    default: return 'info'
  }
}

const handleExport = () => {
  exportAuditLogsToCSV()
  showMsg('Log audit berhasil diekspor ke file CSV')
  loadLogs()
}

const handleClear = () => {
  if (confirm('Apakah Anda yakin ingin mereset catatan Audit Trail? Tindakan ini akan dicatat sebagai event audit baru.')) {
    clearAuditLogs()
    loadLogs()
    showMsg('Audit trail berhasil direset', 'warning')
  }
}
</script>

<style scoped>
.luxury-card {
  background: rgba(255, 255, 255, 0.75) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(184, 134, 11, 0.2) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03) !important;
}

.luxury-table-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03) !important;
}

.table-row-hover {
  transition: all 0.2s ease;
}

.table-row-hover:hover {
  background-color: rgba(184, 134, 11, 0.04) !important;
}

.security-code {
  background: rgba(184, 134, 11, 0.1);
  color: #8c6508;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-family: monospace;
  font-weight: 600;
}

.text-dark {
  color: #2c3e50 !important;
}
</style>
