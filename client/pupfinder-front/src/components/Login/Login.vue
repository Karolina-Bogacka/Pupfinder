<template>
  <div>
    <div class="grid max-h-screen place-items-center">
    <form novalidate @submit.prevent="onSubmit()" class="w-11/12 p-12 bg-white sm:w-8/12 md:w-1/2 lg:w-5/12">
      <h1 class="text-xl font-semibold">Login</h1>
      <div class="flex justify-between gap-3">
      <span class="w-1/2">
        <label class="block mt-2 text-xs font-semibold text-gray-600 uppercase" for="username">Username</label>
        <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" type="text" id="username" v-model="username" />
      </span>
      <span class="w-1/2">
        <label class="block mt-2 text-xs font-semibold text-gray-600 uppercase" for="password">Password</label>
        <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" type="password" id="password" v-model="password"/>
      </span>
      </div>
      <div class="form-group">
        <input class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-green-800 hover:shadow-none" type="submit" value="Login" />&nbsp;
      </div>
        <div class="form-group">
        <router-link class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-red-800 hover:shadow-none" to="/">Cancel</router-link>
        <router-link class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-yellow-300 hover:shadow-none" to="/register">Sign In</router-link>
      </div>
      <div class="form-group">
        <br/>
        <h4 class="text-xl font-semibold">{{message}}</h4>
      </div>
    </form>
  </div>
  </div>
</template>

<script>

  import store from "../../store";
  import axios from "axios";
  import router from "../../router";

  export default {
    name: "Login",
    data() {
      return {
        username: "",
        password: "",
        message: ""
      }
    },
    methods: {
      onSubmit() {
        if (this.username === '' && this.password === '') {
          alert('Review is incomplete. Please fill out every field.');
          return
        } else {
          var report = {
            username: this.username,
            password: this.password,
          }
          //store.dispatch("login", report);
          this.login(report);
          console.log(report);

          this.password = '';
          this.username = '';
        }
      },
    async login(model) {
      try {
        const params = new URLSearchParams()
        params.append('username', model.username)
        params.append('password', model.password)
        var result = await axios.post('http://localhost:8000/api/auth/token', params, {headers: {
            'Content-Type': 'application/x-www-form-urlencoded'}});
        if (result.data) {
          var data = JSON.parse(atob(result.data.access_token.split('.')[1]));
          data['token'] = result.data.access_token;
          store.commit("setToken", data);
          await router.push("/");
        } else {
          store.commit("setError", "Authentication Failed");
        }
      } catch(error){
        this.message="You failed to log in"
        store.commit("setError", "Failed to login");
      } finally {
        store.commit("clearBusy");
      }
    }
  }}
</script>
