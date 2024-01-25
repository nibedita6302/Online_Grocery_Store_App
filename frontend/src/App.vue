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

