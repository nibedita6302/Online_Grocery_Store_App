<template>
    <div id='top' class="row row-cols-1 row-cols-md-3 g-2">
        <div v-if="!this.GET_SEARCH_OUTPUT.length && !this.GET_CATEGORY_ID">
            <h3>No Products Found!</h3>
            <em>Please check for any spelling mistakes...</em>
        </div>
        <div v-for="p in this.get_products()" class="col-3">
            <div class="card h-100">
                <img :src="get_url(p.p_image)" class="card-img-top" :alt="p.p_image">
                <div class="card-body">
                    <h5 class="card-title">{{ p.p_name }}</h5>
                    <em class="card-text">{{ p.brand }}</em>
                    <p class="card-text">{{p.p_description}} | {{p.p_qty}} {{p.unit}} | ₹{{p.price}} </p>
                    <p v-if="p.stock_remaining>5" class="card-text" style="color:green;">In Stock</p>
                    <p v-else-if="p.stock_remaining>0" class="card-text" style="color:red;">
                        Only few left!
                    </p>
                    <p v-else class="card-text" style="color:red;">Out of Stock</p>
                    <form v-if="this.GET_USER_ROLE=='customer'">
                        <input type="number" value="1" min="1" :max="p.stock_remaining" required/>
                        <button class="btn btn-warning" @click="addToCart" :disabled="p.stock_remaining==0">
                            Add to Cart
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
    name: 'ProductList',
    data() {
        return {}
    },
    methods:{
        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        get_products(){
            // if product under category
            if (this.GET_CATEGORY_ID!=null){
                console.log('fetch call products',this.GET_PRODUCT_LIST);
                return this.GET_PRODUCT_LIST;
            // if product under Search
            }else if (this.showProducts){ 
                console.log('search output'); 
                return this.GET_SEARCH_OUTPUT;
            }
        },
        addToCart(){

        }
    },
    computed:{
        ...mapGetters('auth',['GET_USER_ROLE']),
        ...mapGetters('searching',['GET_SEARCH_OUTPUT']),    
        ...mapState('searching',['showProducts']),   
        ...mapGetters('product_display',['GET_CATEGORY_ID','GET_PRODUCT_LIST']) 
    },
    beforeRouteLeave(to, from, next){
        
    }
}
</script>

<style scoped>
    img {
        max-height: 150px;
        max-width: 200px;
    }
    #top {
        padding: 40px;
    }
</style>
  
