<template>
    <div v-show="this.showProducts" @backToHome="showHome" class="container" id="search">
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
    ...mapMutations('searching',['TOGGLE_SEARCH_OUTPUT'])
  },
  computed: {
    ...mapState('searching',['showProducts'])
  },
  beforeRouteLeave(to, from, next){
    console.log('somewhere here',to,from)
    this.TOGGLE_SEARCH_OUTPUT({
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
  