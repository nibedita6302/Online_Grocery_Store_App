<template>
    <div  class="modal fade " id="formModal2" 
        tabindex="-1" aria-labelledby="formModal2Label" >
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
    <div class="container">
        <form id="catg-form"  @submit.prevent="selectApi">
            <legend>Update Category: {{this.GET_FORM_DATA.c_name}}</legend>
            <div v-for="f in form_fields" class="mb-3">
                <label :for="f.id">{{ f.label }}:</label>
                <input v-if="f.type=='file'" :type="f.type" :id="f.id" accept="image/*" >
                <input v-else :type="f.type" :id="f.id" 
                    :placeholder="this.GET_FORM_DATA[f.id]" 
                    v-model="f.data" />
            </div>
            <button type="submit" class="btn btn-success" 
            data-bs-toggle="modal" data-bs-target="#formModal2"
            @click="selectApi">Confirm</button>
        </form>
    </div>          
</template>

<script>
import { mapGetters } from 'vuex';

export default{
    props: {
        'action': String
    },
    name: 'CategoryForm',
    data(){
        return {
            form_fields: [
                {label: 'Category Name', type:'text', id:'c_name', data:''},
                {label: 'Category Image', type:'file', id:'c_image'}
            ],
            msg: 'Operation Successful!'
        }
    },
    methods:{
        selectApi(){
            if (this.$props.action=='PUT'){
                var formData = new FormData()
                const image = document.getElementById('c_image')
                if (image && image.files.length>0) {
                    formData.append("c_image",image.files[0]);
                }
                for(let f in this.form_fields){
                    if (this.form_fields[f].type!=='file') {
                        formData.append(this.form_fields[f].id,this.form_fields[f].data);
                    }
                }
                if (this.$props.action=='PUT'){
                    // console.log('called update');
                    this.updateCategory(formData);
                }else{ this.createCategory(formData); }
            }
        },
        async updateCategory(newData){
            /* console.log('start')
            for (var key of newData.entries()){
                console.log(key[0]+" "+key[1])
            } */
            await fetch('http://10.0.2.15:8000/api/category/'+this.GET_FORM_DATA.c_id+
                    '/edit?auth_token='+this.GET_USER_TOKEN, {
                method: 'PUT',
                body: newData,
                credentials: 'include'
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                if (data.message) {this.msg = data.message;}
            }).catch((error)=>console.log(error.message))
        },
        async createCategory(newData){

        }
    },
    computed:{
        ...mapGetters('auth',['GET_USER_TOKEN']),
        ...mapGetters('formdata',['GET_FORM_DATA'])
    },

}
</script>

<style scoped>
    legend{
        font-weight: bold;
        font-style: italic;
    }
    form{
        border: 2px solid;
        padding: 20px;
        background-color: #d7f5c4;
    }  
</style>