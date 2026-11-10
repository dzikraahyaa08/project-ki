import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'luxuryTheme',
    themes: {
      luxuryTheme: {
        dark: false,
        colors: {
          primary: '#B8860B', // Elegant Gold
          secondary: '#5C5C5C', // Soft Grey
          background: '#F5F2ED', // Soft Alabaster/Champagne
          surface: '#FFFFFF', // Pure White for cards
          error: '#D32F2F',
          info: '#1976D2',
          success: '#388E3C',
          warning: '#F57C00',
        }
      }
    }
  }
})

createApp(App).use(router).use(vuetify).mount('#app')
