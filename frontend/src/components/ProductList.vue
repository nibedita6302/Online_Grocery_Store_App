<template>
    <div  class="modal fade " id="formModal3" 
        tabindex="-1" aria-labelledby="formModal3Label" >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body ">
                    <p>{{ this.msg }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <ProductForm v-if="this.show_product_update_form" :action="this.action"/>
    
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
                    <form v-if="this.GET_USER_ROLE=='customer'" @submit.prevent="addToCart(p.p_id)">
                        <input type="number" value="1" min="1" :max="p.stock_remaining"
                         v-model="this.bought_qty" required/>
                        <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#formModal3"
                        :disabled="p.stock_remaining==0">
                            Add to Cart
                        </button>
                    </form>
                    <div v-if="this.GET_USER_ROLE=='store_manager' && this.GET_USER_ID==p.creator">
                        <button type="submit" class="btn btn-warning me-2" 
                        @click="selectApi_byRole('PUT',p)">
                            <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                            </svg>
                        Update</button>
                        <button type="submit" class="btn btn-danger" 
                        data-bs-toggle="modal" data-bs-target="#formModal3"
                        @click="selectApi_byRole('DELETE',p)">
                            <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                                <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                            </svg>
                        Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ProductForm from './ProductForm.vue';
import { mapGetters, mapState, mapMutations } from 'vuex';

export default {
    name: 'ProductList',
    data() {
        return {
            show_product_update_form: false,
            action: null,
            msg: 'Operation Successful',
            bought_qty: null
        }
    },
    components:{
        ProductForm,
    },
    methods:{
        ...mapMutations('formdata',['STORE_FORM_DATA']),

        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        get_products(){
            // if product under category
            if (this.GET_CATEGORY_ID!=null){
                // console.log('fetch call products',this.GET_PRODUCT_LIST);
                return this.GET_PRODUCT_LIST;
            // if product under Search
            }else if (this.showProducts){ 
                // console.log('search output'); 
                return this.GET_SEARCH_OUTPUT;
            }
        },
        selectApi_byRole(action,p){
            if (action=='PUT'){
                this.STORE_FORM_DATA({
                    data: p
                })
                this.action='PUT';
                this.show_product_update_form=true;
                // this.p_id=p_id;
            }else{
                this.deleteProduct(p.p_id);
            }
        },
        async addToCart(p_id){
            await fetch('http://10.0.2.15:8000/api/customer/'+
                        this.GET_USER_ID+'/add/product/'+p_id+'?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                mode: 'cors',
                body: JSON.stringify({'bought_qty':this.bought_qty}),
                headers:{
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Delete Product:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.msg = data.message;
            }).catch((error)=>{console.log(error);})
        },
        async deleteProduct(p_id){
            await fetch('http://10.0.2.15:8000/api/product/'+p_id+
                        '/delete?auth_token='+this.GET_USER_TOKEN, {
                method: 'DELETE',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Delete Product:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.msg = data.message;
            }).catch((error)=>{console.log(error);})
        },
    },
    computed:{
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_ID', 'GET_USER_TOKEN']),
        ...mapGetters('searching',['GET_SEARCH_OUTPUT']),    
        ...mapState('searching',['showProducts']),   
        ...mapGetters('product_display',['GET_CATEGORY_ID','GET_PRODUCT_LIST']) 
    },/* 
    beforeRouteLeave(to, from, next){
        
    } */
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
  
