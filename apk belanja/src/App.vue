<template>
  <router-view></router-view>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Global Styles */
html, body {
  margin: 0;
  padding: 0;
  background-color: #F5F2ED;
  color: #2C3E50;
  font-family: 'Outfit', sans-serif;
}

/* Custom Scrollbar for luxury feel */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #F5F2ED;
}
::-webkit-scrollbar-thumb {
  background: #D4AF37;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #B8860B;
}
</style>
