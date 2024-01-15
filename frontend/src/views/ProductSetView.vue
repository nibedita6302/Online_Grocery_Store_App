<template>
  <div 
    v-show="this.showProducts||this.onClickCategory" 
    @backToHome="showHome" 
    class="container" 
    id="search">
      <ProductList />
  </div>
</template>
  
<script>
import ProductList from '../components/ProductList.vue';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'ProductSetView',
  data(){
    return {}
  },
  components:{
    ProductList
  },
  methods:{
    ...mapMutations('searching',['TOGGLE_SEARCH_OUTPUT']),
    ...mapMutations('product_display',['TOGGLE_ONCLICK_CATEGORY'])
  },
  computed: {
    ...mapState('searching',['showProducts']),
    ...mapState('product_display',['onClickCategory'])
  },
  beforeRouteLeave(to, from, next){
    console.log('somewhere here',to,from)
    this.TOGGLE_SEARCH_OUTPUT({
        setTo: false
    });
    console.log('productlist',to,from)
    this.TOGGLE_ONCLICK_CATEGORY({
        setTo: false
    });
    next();
  }
}
</script>
<style scoped>
  #search{
    padding: 10px;
  }
</style>
  