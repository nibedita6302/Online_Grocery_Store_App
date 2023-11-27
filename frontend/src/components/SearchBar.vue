<template>
    <nav class="navbar">
        <div class="container">
            <a ></a>
            <form class="container-fluid">
                <div class="input-group">
                    <span class="navbar-brand" id="basic-addon1">Grocery Store</span>
                    <input class="form-control" type="search" placeholder="Search" 
                    aria-label="Search" aria-describedby="basic-addon1">
                    <button class="btn btn-outline-dark" type="submit">Search</button>
                </div>
            </form>
        </div>  
    </nav>
</template>

<script>
    export default {
        name: 'SearchBar'
    }   
</script>
  
<style scoped>
    nav {
        background-color: rgb(36, 235, 36);
    }
    span {
        font-weight: 800;
        font-size: x-large;
        color: black;
    }
    button {
        background-color: white;
        color: black;
    }
</style>