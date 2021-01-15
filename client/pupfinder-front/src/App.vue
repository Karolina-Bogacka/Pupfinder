<template>
  <div>
    <button v-if="state" @click="logout">Logout</button>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data(){
    return{
      state: false
    }
  },
  computed: {
    state(){
      return this.$store.getters.isAuthenticated
    }
  },
  methods:{
    logout(){
      this.$store.commit("clearToken")
      this.$router.push('/')
    }
  },
  components: {
  }
}
//background-image: url("./assets/PUPFINDER.png");
</script>

<style>
body {
  background-color: #247510;
  background-repeat: no-repeat;
}
</style>
