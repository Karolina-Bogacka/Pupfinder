<template>
  <div>
  <img alt="Pupfinder logo" src="./assets/PUPFINDER.png" />
    <Body/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Body from './components/Body/Body.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Body
  }
}
</script>
