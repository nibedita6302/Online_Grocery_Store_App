<template>
  <div v-if="this.p_review===null"
    v-show="(this.showProducts||this.onClickCategory)" 
    class="container" 
    id="search">
      <ProductList />
  </div>
  <div v-if="this.p_review!==null"
      class="container">
    <ProductReview />
  </div>
</template>
  
<script>
import ProductList from '../components/ProductList.vue';
import ProductReview from '../components/ProductReview.vue';
import {mapMutations, mapState} from 'vuex';

export default {
  name: 'ProductSetView',
  data(){
    return {}
  },
  components:{
    ProductList,
    ProductReview
  },
  methods:{
    ...mapMutations('searching',['TOGGLE_SEARCH_OUTPUT']),
    ...mapMutations('product_display',['TOGGLE_ONCLICK_CATEGORY','SET_REVIEW_P_ID'])
  },
  computed: {
    ...mapState('searching',['showProducts']),
    ...mapState('product_display',['onClickCategory','p_review'])
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
    console.log('product review',to,from)
    this.SET_REVIEW_P_ID({
        p_id: null
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
  