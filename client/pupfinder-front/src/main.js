import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './index.css'


const app = createApp(App);
app.use(VueAxios,axios);
app.config.globalProperties.$center = [52.237049, 21.017532];
app.mount('#app');
