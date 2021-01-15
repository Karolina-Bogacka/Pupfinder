import { createWebHistory, createRouter } from "vue-router";
import Body from "./components/Body/Body.vue";
import Form from "./components/Form/Form.vue";
import Login from "./components/Login/Login.vue";
import store from "./store/index.js"
import Register from "./components/Register/Register.vue";

const authGuard = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
  } else {
    next("/login")
  }
};

const routes = [
  {
    path: "/",
    name: "LocalMap",
    component: Body,
  },
  {
    path: "/report",
    name: "ReportPuppy",
    component: Form,
    beforeEnter: authGuard
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
    {
    path: '/register',
    name: 'Register',
    component: Register
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.afterEach(() => {
  store.commit("clearError");
});

export default router;
