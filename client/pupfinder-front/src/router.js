import { createWebHistory, createRouter } from "vue-router";
import Body from "./components/Body/Body.vue";
import Form from "./components/Form/Form.vue";

const routes = [
  {
    path: "/",
    name: "LocalMap",
    component: Body,
  },
  {
    path: "/report",
    name: "ReportPuppy",
    component: Form
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
