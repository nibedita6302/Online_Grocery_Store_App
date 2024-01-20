<template>
    <div class="text-center p-3">
        <button v-show="this.GET_USER_ROLE=='store_manager'"
        type="submit" class="btn btn-outline-primary border-4 me-4" 
        @click="show_form(1)">
            <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>
            Create Product
        </button>

        <button v-show="this.GET_USER_ROLE=='admin'"
        type="submit" class="btn btn-outline-success border-4 me-4" 
        @click="show_form(2)">
            <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>
            Create Category
        </button> <hr>
    </div>
    <ProductForm v-if="this.createForm===1" action="POST"/>
    <CategoryForm v-else-if="this.createForm===2" action="POST"  /> 
</template>

<script>
import { mapGetters } from 'vuex';
import ProductForm from './ProductForm.vue';
import CategoryForm from './CategoryForm.vue';

export default {
    name: 'CreateInventory',
    data() {
        return { 
            createForm: null
        }
    },
    components:{
        ProductForm,
        CategoryForm
    },
    methods:{
        show_form(i){
            if (this.createForm===i){
                this.createForm=null;
            }else{
                this.createForm=i;
            }
        },
/*         async createCategory(){
            
        },
        async createProduct(){

        } */
    },
    computed:{
        ...mapGetters('auth',['GET_USER_ROLE'])
    }
}
</script>