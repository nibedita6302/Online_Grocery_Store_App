import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'
import mitt from 'mitt'

export const emitter = mitt(); 
const app = createApp(App);
app.use(router);
app.use(store);
// app.config.globalProperties.emitter = emitter;
app.mount('#app');
