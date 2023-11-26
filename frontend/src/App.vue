<template>
  <div id="main">
    <Navbar />
    <SearchBar />
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import SearchBar from './components/SearchBar.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    SearchBar
  }
}

</script>

<style scoped>
  /* #main{
    background-image: url('./assets/background.jpg');
    background-repeat: no-repeat;
    background-size: contain;
    height: 100vh;
  } */
</style>
