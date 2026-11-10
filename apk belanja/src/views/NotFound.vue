<template>
  <v-app>
    <v-main class="d-flex align-center justify-center bg-background">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="5">
            <v-card class="elevation-0 rounded-xl luxury-card text-center py-12 px-6">
              <div class="luxury-404-number">404</div>
              
              <v-card-title class="text-h5 font-weight-bold luxury-title mb-2 justify-center">
                Halaman Tidak Ditemukan
              </v-card-title>
              
              <v-card-text class="text-secondary font-weight-medium mb-8 px-4">
                Maaf, halaman yang Anda cari tidak dapat ditemukan atau telah dipindahkan.
              </v-card-text>
              
              <v-btn
                color="primary"
                size="large"
                to="/"
                class="font-weight-bold rounded-lg px-8 text-none elevation-0"
              >
                <v-icon start class="mr-2">mdi-home</v-icon>
                Kembali ke Beranda
              </v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
// No complex logic needed for static 404 page
</script>

<style scoped>
.bg-background {
  background-color: #F5F2ED !important;
  background-image: radial-gradient(circle at 50% -20%, #ffffff 0%, transparent 70%);
  min-height: 100vh;
}

.luxury-card {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.8) !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05) !important;
  transition: box-shadow 0.4s ease, transform 0.4s ease;
  position: relative;
  overflow: hidden;
}

.luxury-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

.luxury-card:hover {
  box-shadow: 0 20px 45px rgba(184, 134, 11, 0.08) !important;
  transform: translateY(-2px);
}

.luxury-404-number {
  font-size: 8rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -2px;
  background: linear-gradient(45deg, #B8860B, #D4AF37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 5px 20px rgba(184, 134, 11, 0.2);
  margin-bottom: 1rem;
  font-family: 'Outfit', sans-serif;
}

.luxury-title {
  letter-spacing: 2px;
  color: #333333;
}
</style>
