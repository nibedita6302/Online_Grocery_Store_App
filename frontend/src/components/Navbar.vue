<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <!-- Toggle Button -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" 
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link active-class="active" class="nav-link" aria-current="page" to="/" @click="refresh">
              Home</router-link>  
          </li>
          <li class="nav-item">
            <router-link to='/offers' active-class="active" class="nav-link">Offers</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/my-cart' v-if="this.GET_USER_ROLE=='customer'" 
            active-class="active" class="nav-link">My Cart</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.GET_USER_ROLE=='customer'" 
            active-class="active" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.GET_USER_ROLE=='customer'" 
            active-class="active" class="nav-link">Orders</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/requests' v-if="this.GET_USER_ROLE=='admin'||this.GET_USER_ROLE=='store_manager'"
             active-class="active" class="nav-link">Requests </router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.GET_USER_ROLE=='admin'" active-class="active" class="nav-link">
              Logs & Reports
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <LogoutAlert />
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import LogoutAlert from './LogoutAlert.vue'
import {mapGetters} from "vuex"

export default {
  name: 'Navbar',
  data(){
    return {}
  },
  components:{
    LogoutAlert
  },
  methods:{
    refresh(){
      const router = this.$router
      router.push('/')
    }
  },
  computed:{
    ...mapGetters('auth',['GET_USER_ROLE'])
  },
  mounted() {
  }
}
</script>

<style scoped>
  .active {
    border-bottom: 2px solid white;
  }
</style>
 

