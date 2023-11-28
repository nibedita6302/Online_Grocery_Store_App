<template>
  <CategoryList v-show="showCat" @showProducts="listenShow"/>
  <ProductList v-if="showProd==true" :c_id="c_id"  />
</template>

<script>
import CategoryList from '../components/CategoryList.vue'
import ProductList from '../components/ProductList.vue'

export default {
  name: 'HomeView',
  data(){
    return {
      c_id: 0,
      showCat: true,
      showProd: false
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
    }
  },
  mounted() {
      this.emitter.on("searchProducts", () => {
          this.showCat = false;
          this.showProd=true;
          // console.log('home')
      });
  }
}
</script>
