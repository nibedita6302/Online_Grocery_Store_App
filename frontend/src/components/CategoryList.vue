<template>
    <div  class="modal fade " id="formModal1" 
        tabindex="-1" aria-labelledby="formModal1Label" >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body ">
                    <h5>{{ this.msg }}</h5>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div id='top' class="row g-2">
        <div v-for="c in filteredCategory" class="col-4">
            <div class="card bg-dark text-white h-100">
                <img :src="get_url(c.c_image)" class="card-img-top" :alt="c.c_image">
                <div class="card-img-overlay">
                    <h3 class="card-title" @click="categoryClicked(c.c_id)">
                        <router-link to="/show-products" 
                        class="text-white text-decoration-none">{{ c.c_name }}</router-link>
                    </h3>
                </div>
                <div v-show="this.GET_USER_ROLE=='admin'" class="card-footer text-center">
                    <button type="submit" class="btn btn-warning me-2" 
                    @click="selectApi_byRole('PUT',c)">
                        <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                        <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                        </svg>
                    Update</button>
                    <button type="submit" class="btn btn-danger" 
                    data-bs-toggle="modal" data-bs-target="#formModal1"
                    @click="selectApi_byRole('DELETE',c)">
                        <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                            <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                        </svg>
                    Delete</button>
                </div>
            </div>
        </div>
    </div>
    <CategoryForm v-if="show_category_update_form" :action="this.action"  /> 
</template>

<script>
import CategoryForm from './CategoryForm.vue';
import { mapGetters, mapMutations } from 'vuex';

export default {
    name: 'CategoryList',
    data() {
        return {
            categories: [],
            show_category_update_form: false,
            action: '',
            msg: 'Operation Successful!'
        }
    },
    components:{
        CategoryForm
    },
    methods:{
        ...mapMutations('product_display',['SET_CATEGORY_ID','STORE_PRODUCT_LIST']),
        ...mapMutations('formdata',['STORE_FORM_DATA']),

        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        allowCRUD(){
            /* console.log(this.GET_USER_ROLE) */
            if(this.GET_USER_ROLE=='admin'||this.GET_USER_ROLE=='store_manager') { return true }
            return false
        },
        async categoryClicked(id){ // on category click
            const prodList = await this.get_products_under_category(id); //fetch product under c_id
            // console.log(prodList,'productList')
            this.STORE_PRODUCT_LIST({ //store to product_display
                productList: prodList
            })
            this.SET_CATEGORY_ID({  // store category id
                c_id: id 
            })
        },
        selectApi_byRole(action,c){
            // console.log('in')
            if (this.GET_USER_ROLE=='admin'){
                if (action=='PUT'){
                    this.show_category_update_form=true;
                    this.action='PUT';
                    this.STORE_FORM_DATA({
                        data: c
                    })
                }else{
                    this.deleteCategory(c.c_id);
                }
            }else{
                this.sendApproval();
            }
        },
        async getAllCategory(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/category', {
                    credentials: 'include'
                });
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList - GetAll: "+ res.status);
                }
                const data = await res.json();
                this.categories = data;
            }catch(error) {
                console.log(error);
            }
            return null;
        },
        async deleteCategory(c_id){
            await fetch('http://10.0.2.15:8000/api/category/'+c_id+
                        '/delete?auth_token='+this.GET_USER_TOKEN, {
                method: 'DELETE',
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList - Delete: "+ res.status);
                }
                return res.json()
            }).then((data)=>{
                this.msg = data.message;
                console.log(this.msg)
            }).catch((error)=>{console.log(error);})
        },
        async sendApproval(){

        },
        async get_products_under_category(c_id){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/product/category/'+c_id,{
                    credentials: 'include'
                });
                if (!res.ok) {
                    throw Error("HTTP Error at ProductList: "+ res.message+" "+ res.status);
                }
                const data = await res.json();
                // console.log(data);
                return data;
            }catch(error) {
                console.log(error);
            }
        }  
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_TOKEN']),
        filteredCategory(){
            return this.categories.filter(c => c.product_count>0||this.allowCRUD())
        }
    },
    mounted() { 
        this.getAllCategory();
    }
}
</script>

<style scoped>
    #top {
        padding: 30px;
    }
    h3{
        text-align: center;
    }
    #in-btn{
        height: 20px;
        width: 15px;
    }
    #out-btn{
        height: 25px;
        width: 25px;
    }
    button{
        z-index: 2;
        position: relative;
    }
    img{
        max-height: 250px;
        max-width: 450px;
    }
    router-link{
        color: white;
    }
</style>
  
 
