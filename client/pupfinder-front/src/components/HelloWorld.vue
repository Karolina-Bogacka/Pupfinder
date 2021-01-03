<template>
  <h1>{{ msg }}</h1>
  <button @click="count++">count is: {{ count }}</button>
  {{info}}
  <p>Edit <code>components/HelloWorld.vue</code> to test hot module replacement.</p>
</template>

<script>
import axios from "axios";

var newInfo = ";"
axios.get('http://localhost:8000/').then(response => (newInfo = response.data));
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      count: 0,
      info: newInfo
    }
  },
  mounted(){
    axios.get('http://localhost:8000/').then(response => (this.info = response.data))
  }
}
</script>
