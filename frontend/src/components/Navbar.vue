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
            <router-link to='#' active-class="active" class="nav-link">Features</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' active-class="active" class="nav-link">Features</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' active-class="active" class="nav-link">Features</router-link>
          </li>
          <li class="nav-item">
            <router-link to='#' active-class="active" class="nav-link">Features</router-link>
          </li>
          <li class="nav-item">
            <router-link to='/login' active-class="active" class="nav-link">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
  .active {
    border: 1px solid white;
  }
</style>

