<template>
  <div>
    <h1>Login</h1>
    <form novalidate @submit.prevent="onSubmit()">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" class="form-control" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" class="form-control" />
      </div>
      <div class="form-group">
        <input type="submit" class="btn btn-success" value="Login" />&nbsp;
        <router-link class="btn btn-info" to="/">Cancel</router-link>
      </div>
    </form>
    <h4>{{message}}</h4>
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
        console.log(result);
        if (result.data) {
          var data = JSON.parse(atob(result.data.access_token.split('.')[1]));
          data['token'] = result.data.access_token;
          store.commit("setToken", data);
          await router.push("/");
          console.log(data.exp*1000);
          console.log(Date.now());
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
