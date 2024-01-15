<template>
  <CreateInventory v-if="this.GET_USER_ROLE=='admin'||this.GET_USER_ROLE=='store_manager'"/>
  <div v-show="!this.showProducts">
    <CategoryList/>
    <!-- <ProductList v-if="showProd==true" :c_id="c_id" /> -->
  </div>
  <div v-show="this.showProducts" class="container" id="search"> 
    <ProductSetView />
  </div>
</template>

<script>
import CategoryList from '../components/CategoryList.vue';
import CreateInventory from '@/components/CreateInventory.vue';
import ProductSetView from './ProductSetView.vue';
// import {emitter} from '../main.js'
import {mapGetters, mapState} from 'vuex';

export default {
  name: 'HomeView',
  data(){
    return {
      c_id: 0,
      showProd: false
    }
  },
  components:{
    CategoryList,
    CreateInventory,
    ProductSetView
},
  methods:{
    /*listenShow(c_id){
      this.c_id=c_id;
      this.showProd=true;
      console.log('inhere'+this.c_id)
      emitter.off("showProducts", this.listenShow);
    } */
  },
  computed: {
    ...mapState('searching',['showProducts']),
    ...mapGetters('auth',['GET_USER_ROLE']),
  }
/*   mounted() {
      emitter.on("showProducts", this.listenShow);
  } */
}
</script>

<style scoped>
  
</style>
