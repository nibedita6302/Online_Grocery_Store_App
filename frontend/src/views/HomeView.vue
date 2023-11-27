<template>
  <CategoryList @showProducts="listenShow"/>
  <ProductList v-if="c_id!==null" :c_id="c_id"  />
</template>

<script>
import CategoryList from '../components/CategoryList.vue'
import ProductList from '../components/ProductList.vue'

export default {
  name: 'HomeView',
  data(){
    return {
      c_id: null
    }
  },
  methods:{
    listenShow(c_id){
      this.c_id=c_id;
      console.log('inhere'+this.c_id)
    }
  },
  components:{
    ProductList,
    CategoryList
  }
}
</script>
