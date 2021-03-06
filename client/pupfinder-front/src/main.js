import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './index.css'
import router from "./router.js";
import store from "./store";

const app = createApp(App);
app.use(VueAxios,axios);
app.use(router);
app.use(store);
app.config.globalProperties.$center = [52.237049, 21.017532];
app.mount('#app');
