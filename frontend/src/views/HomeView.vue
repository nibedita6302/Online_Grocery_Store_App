<template>
  <div v-show="!this.is_search">
    <CategoryList @showProducts="listenShow"/>
    <ProductList v-if="showProd==true" :c_id="c_id" />
  </div>
  <div v-show="this.is_search" @backToHome="showHome" class="container" id="search">
    <!-- aria-label="..." on the control -->
    <button type="button" class="btn btn-dark" @click="showHome">
      <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" class="bi bi-arrow-left-circle-fill" viewBox="0 0 16 16">
        <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z"/>
      </svg>
    Back To Home</Button>
    <ProductList />
  </div>
</template>

<script>
import CategoryList from '../components/CategoryList.vue'
import ProductList from '../components/ProductList.vue'

export default {
  name: 'HomeView',
  data(){
    return {
      c_id: 0,
      showProd: false,
      is_search: false
    }
  },
  components:{
    ProductList,
    CategoryList
  },
  methods:{
    listenShow(c_id){
      this.c_id=c_id;
      this.showProd=true;
      console.log('inhere'+this.c_id)
    },
    showHome(){
      this.is_search = false;
      console.log('search false')
    }
  },
  mounted() {
      this.emitter.on("searchProducts", () => {
          this.is_search = true;
          console.log('search true')
      });
  }
}
</script>

<style scoped>
  svg{
    height: 25px;
    width: 30px;
  }
  #search{
    padding: 10px;
  }
</style>
