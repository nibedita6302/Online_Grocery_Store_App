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
            <router-link active-class="active" class="nav-link" aria-current="page" to="/">Home</router-link>  
          </li>
          <li class="nav-item">
            <router-link to='#' active-class="active" class="nav-link">Offers</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.user.role=='customer'||this.user.role===null" 
            active-class="active" class="nav-link">My Cart</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.user.role=='customer'||this.user.role===null" 
            active-class="active" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.user.role=='admin'||this.user.role=='store_manager'"
             active-class="active" class="nav-link">Approvals </router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' v-if="this.user.role=='admin'" active-class="active" class="nav-link">
              Logs & Reports
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Logout</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data(){
    return {
      user: null
    }
  },
  created(){
    const user=localStorage.getItem('user');
    // console.log(user)
    this.user = JSON.parse(user)[0];
  }
}
</script>

<style scoped>
  .active {
    border-bottom: 2px solid white;
  }
</style>
 

