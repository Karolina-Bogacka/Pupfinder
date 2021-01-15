<template>
  <div>
    <h4>Register</h4>
    <form @submit.prevent="register">
      <label for="username">Username</label>
      <div>
          <input id="username" type="text" v-model="username" required autofocus>
      </div>

      <label for="email" >E-Mail Address</label>
      <div>
          <input id="email" type="email" v-model="email" required>
      </div>

      <label for="password">Password</label>
      <div>
          <input id="password" type="password" v-model="password" required>
      </div>

      <label for="password-confirm">Confirm Password</label>
      <div>
          <input id="password-confirm" type="password" v-model="password_confirmation" required>
      </div>

      <div>
          <button type="submit">Register</button>
          <router-link class="btn btn-info" to="/login">Cancel</router-link>
          <router-link class="btn btn-info" to="/">Home</router-link>
      </div>
    </form>
    <h4>{{message}}</h4>
  </div>
</template>

<script>
export default {
  name: "Register",
  data(){
    return{
      username: "",
      email: "",
      password: "",
      password_confirmation: "",
      message: ""
    }
  },
  methods: {
      register: function () {
        if(this.password === this.password_confirmation){
        let data = {
          username: this.username,
          email: this.email,
          password: this.password
        }
        this.$store.dispatch('register', data);
        this.$router.push('/login');
      }else{
        this.message = "Confirm Password!";
    }}
    }
}
</script>

<style scoped>

</style>
