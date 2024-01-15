<template>
    <div id='top' class="row g-2">
        <div v-for="c in categories" class="col-4">
            <div v-if="c.product_count>0||allowCRUD()" class="card bg-dark text-white h-100"  >
                <img :src="get_url(c.c_image)" class="card-img-top" :alt="c.c_image">
                <div class="card-img-overlay">
                    <h3 class="card-title stretched-link" @click="categoryShow(c.c_id)">
                        {{ c.c_name }}
                    </h3>
                </div>
                <div v-show="allowCRUD()" class="card-footer text-center">
                    <button type="submit" class="btn btn-warning me-2" 
                    @click="selectApi_byRole('PUT',c.c_id)">
                        <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                           <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
                        </svg>
                    Update</button>
                    <button type="submit" class="btn btn-danger" 
                    @click="selectApi_byRole('DELETE',c.c_id)">
                        <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                            <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                        </svg>
                    Delete</button>
                </div>
            </div>
        </div>
    </div>
    <CategoryForm v-if="show_category_update_form" :action="this.action" :c_id="c_id" />
</template>

<script>
import CategoryForm from './CategoryForm.vue';
import {emitter} from '../main.js'
import { mapGetters } from 'vuex';

export default {
    name: 'CategoryList',
    data() {
        return {
            categories: [],
            show_category_update_form: false,
            action: '',
            c_id: null
        }
    },
    components:{
        CategoryForm
    },
    methods:{
        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        allowCRUD(){
            /* console.log(this.GET_USER_ROLE) */
            if(this.GET_USER_ROLE=='admin'||this.GET_USER_ROLE=='store_manager') { return true }
            return false
        },
        categoryShow(c_id){
            // console.log('here')
            emitter.emit('showProducts',c_id);
        },
        selectApi_byRole(action,c_id){
            if (this.GET_USER_ROLE=='admin'){
                if (action=='PUT'){
                    this.show_category_update_form=true;
                    this.action='PUT';
                    this.c_id=c_id;
                }else{
                    this.deleteCategory();
                }
            }else{
                this.sendApproval();
            }
        },
        async deleteCategory(){

        },
        async sendApproval(){

        },
        async getAllCategory(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/category', {
                    credentials: 'include'
                });
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList: "+ res.status);
                }
                const data = await res.json();
                this.categories = data;
            }catch(error) {
                console.log(error);
            }
            return null;
        }   
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE'])
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
        max-height: 300px;
        max-width: 500px;
    }
</style>
  
 
