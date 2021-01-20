<template>
  <div class="grid max-h-screen place-items-center">
    <form @submit.prevent="register" class="w-11/12 p-12 bg-white sm:w-8/12 md:w-1/2 lg:w-5/12">
      <h1 class="text-xl font-semibold">Register</h1>
      <div class="flex justify-between gap-3">
        <span class="w-1/2">
      <label class="block text-xs font-semibold text-gray-600 uppercase" for="username">Username</label>
        <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" id="username" type="text" v-model="username" required autofocus>
        </span>
        <span class="w-1/2">
        <label class="block text-xs font-semibold text-gray-600 uppercase" for="password">Password</label>
          <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" id="password" type="password" v-model="password" required>
        </span>
      </div>
      <div class="flex justify-between gap-3">
        <span class="w-1/2">
      <label class="block text-xs font-semibold text-gray-600 uppercase" for="email" >E-Mail Address</label>
          <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" id="email" type="email" v-model="email" required>
        </span>
      <span class="w-1/2">
      <label class="block text-xs font-semibold text-gray-600 uppercase" for="password-confirm">Confirm Password</label>
          <input class="block w-full p-3 mt-2 text-grey-500 bg-yellow-200 appearance-none focus:outline-none focus:bg-yellow-300 focus:shadow-inner" id="password-confirm" type="password" v-model="password_confirmation" required>
      </span>
      </div>

          <button class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-green-800 hover:shadow-none" type="submit">Register</button>
      <div class="form-group">
      <router-link class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-red-800 hover:shadow-none" to="/login">Cancel</router-link>
          <router-link class="w-full py-3 mt-6 font-medium tracking-widest text-white uppercase bg-green shadow-lg focus:outline-none hover:bg-yellow-300 hover:shadow-none" to="/">Home</router-link>
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
