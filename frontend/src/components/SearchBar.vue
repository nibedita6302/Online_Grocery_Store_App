<template>
    <nav class="navbar">
        <div class="container">
            <a ></a>
            <form class="container-fluid" @submit.prevent="search">
                <div class="input-group">
                    <span class="navbar-brand" id="basic-addon1">Grocery Store</span>
                    <input class="form-control" v-model="search_input" type="search" placeholder="Search" 
                    aria-label="Search" aria-describedby="basic-addon1">
                    <button class="btn btn-outline-dark" type="submit" @click="search">Search</button>
                </div>
            </form>
        </div>  
    </nav>
</template>

<script>
// import {emitter} from '../main.js'

export default {
    name: 'SearchBar',
    data(){
        return {
            search_input: '',
            search_output: '',
            count: 0
        }
    },
    methods:{
        async search(){
            await fetch('http://10.0.2.15:8000/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({string:this.search_input})
            }).then(res => {
                if (!res.ok) { throw Error("HTTP Error at Search:"+res.status) }
                return res.json() ;
            }).then((data) => {
                this.search_output = data;
                this.emitter.emit('searchProducts', this.search_output);
                // console.log('search', this.search_output);
            }).catch( (error) => console.log(error) ) ;
        }
    }
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
