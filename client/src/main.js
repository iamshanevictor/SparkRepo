import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ErrorBoundary from './components/ErrorBoundary.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.component('ErrorBoundary', ErrorBoundary)
app.mount('#app')
