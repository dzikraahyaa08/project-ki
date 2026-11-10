<template>
  <v-app>
    <!-- Navigation Drawer / Sidebar -->
    <v-navigation-drawer v-model="drawer" class="luxury-sidebar" border="none">
      <div class="pa-6 pb-2 text-center">
        <h2 class="font-weight-bold luxury-title">LUXURY</h2>
        <p class="text-caption text-secondary">Store Admin</p>
      </div>

      <v-divider class="mb-4 border-opacity-25" color="primary"></v-divider>

      <v-list nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Dashboard Utama"
          to="/admin/dashboard"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-package-variant"
          title="Kelola Produk"
          to="/admin/products"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-tag-multiple"
          title="Kelola Merek"
          to="/admin/brands"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-cart-check"
          title="Kelola Pesanan"
          to="/admin/orders"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account-group"
          title="Pengguna"
          to="/admin/users"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-shield-check"
          title="Audit Keamanan (A5)"
          to="/admin/audit-logs"
          active-color="primary"
          class="luxury-list-item"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-4">
          <v-btn block color="error" variant="tonal" @click="handleLogout" class="logout-btn">
            <v-icon start>mdi-logout</v-icon>
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar class="luxury-app-bar" elevation="0">
      <v-app-bar-nav-icon @click="drawer = !drawer" color="primary"></v-app-bar-nav-icon>
      <v-app-bar-title class="text-primary font-weight-bold" style="letter-spacing: 1px">{{ route.name }}</v-app-bar-title>
    </v-app-bar>

    <!-- Main Content -->
    <v-main class="bg-background">
      <div class="page-transition-wrap">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { logSecurityEvent } from '../services/security'

const router = useRouter()
const route = useRoute()
const drawer = ref(true)

const handleLogout = () => {
  logSecurityEvent({
    action: 'AUTH_LOGOUT',
    category: 'Authentication',
    severity: 'INFO',
    actor: 'admin',
    details: 'Administrator berhasil keluar dari sistem (Logout manual)'
  })
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  router.push('/login')
}
</script>

<style scoped>
.luxury-sidebar {
  background: rgba(255, 255, 255, 0.85) !important;
  backdrop-filter: blur(20px) !important;
  border-right: 1px solid rgba(184, 134, 11, 0.15) !important;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02) !important;
}

.luxury-list-item {
  border-radius: 12px;
  margin: 4px 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  color: #2C3E50 !important;
}

.luxury-list-item:hover {
  background: rgba(184, 134, 11, 0.08) !important;
  transform: translateX(5px);
  color: #B8860B !important;
}

.luxury-list-item.v-list-item--active {
  background: linear-gradient(90deg, rgba(184, 134, 11, 0.15) 0%, rgba(184, 134, 11, 0.02) 100%) !important;
  border-left: 4px solid #B8860B;
  color: #B8860B !important;
  font-weight: 600;
}

.luxury-title {
  letter-spacing: 5px;
  background: linear-gradient(45deg, #B8860B, #D4AF37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(184, 134, 11, 0.15);
}

.luxury-app-bar {
  background: rgba(245, 242, 237, 0.8) !important;
  backdrop-filter: blur(15px) !important;
  border-bottom: 1px solid rgba(184, 134, 11, 0.1) !important;
}

.logout-btn {
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.logout-btn:hover {
  background: rgba(211, 47, 47, 0.15) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.15);
}

.bg-background {
  background-color: #F5F2ED !important;
  min-height: 100vh;
}

/* Page Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
