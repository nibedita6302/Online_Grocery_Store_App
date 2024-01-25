<template>
  <CreateInventory v-if="this.GET_USER_ROLE=='admin'||this.GET_USER_ROLE=='store_manager'"/>
  <div v-show="!this.showProducts">
    <CategoryList/>
  </div>
  <div v-show="this.showProducts" class="container" id="search"> 
    <ProductSetView />
  </div>
</template>

<script>
import CategoryList from '../components/CategoryList.vue';
import CreateInventory from '@/components/CreateInventory.vue';
import ProductSetView from './ProductSetView.vue';
import {mapGetters, mapMutations, mapState} from 'vuex';

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
  },
  computed: {
    ...mapState('searching',['showProducts']),
    ...mapGetters('auth',['GET_USER_ROLE']),
  }
}
</script>

<style scoped>
  
</style>
