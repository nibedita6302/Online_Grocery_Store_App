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
            <legend v-if="this.GET_FORM_DATA!=null">
                Update Category: {{this.GET_FORM_DATA.c_name}}
            </legend>
            <legend v-else> Create Category </legend>

            <div v-for="f in form_fields" class="mb-3">
                <label :for="f.id">{{ f.label }}:</label>
                <input v-if="f.type=='file'" :type="f.type" :id="f.id" accept="image/*" :required="isRequired">
                <input v-else :type="f.type" :id="f.id" 
                    :placeholder="placeholder(f.id)" 
                    v-model="f.data" :required="isRequired"/>
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
    name: 'CategoryForm',
    props: {
        'action': String
    },
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
        isRequired(){
            if (this.GET_USER_ROLE=='admin'){
                return true
            }
            return false
        },
        placeholder(id){
            if (this.GET_FORM_DATA!=null){
                return this.GET_FORM_DATA[id]
            } return ' '
        },
        selectApi(){
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
            }else{ 
                // console.log('create in')
                this.createCategory(formData); 
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
                if (data!=null) {this.msg = data.message;}
            }).catch((error)=>console.log(error.message))
        },
        async createCategory(newData){
            await fetch('http://10.0.2.15:8000/api/category/create?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                body: newData,
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Create Category:'+res.status)
                }
                return res.json()
            }).then((data)=>{
                if (data!=null) {this.msg = data.message;}
            }).catch((error)=>console.log(error.message))
        },
/*         async requestOnCategory(newData){
            await fetch('http://10.0.2.15:8000/api/requests?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                body: newData,
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Request on Category:'+res.status)
                }
                return res.json()
            }).then((data)=>{
                if (data!=null) {this.msg = data.message;}
            }).catch((error)=>console.log(error.message))
        } */
    },
    computed:{
        ...mapGetters('auth',['GET_USER_TOKEN','GET_USER_ROLE']),
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