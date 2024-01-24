<template>
    <div  class="modal fade " id="requestForm" 
        tabindex="-1" aria-labelledby="requestFormLabel" >
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
    <h2 class="text-center">Send Request</h2>
    <div class="text-center p-3">
        <button type="submit" class="btn btn-outline-success border-2 me-2" 
        @click="selectAction('POST')">
            <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>
            Create Category
        </button>

        <button type="submit" class="btn btn-outline-primary border-2 me-2" 
        @click="selectAction('PUT')">
            <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
                <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
            </svg>
            Update Category
        </button> 

        <button type="submit" class="btn btn-outline-danger border-2 me-2" 
        @click="selectAction('DELETE')">
            <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
            </svg>
            Delete Category
        </button> <hr>
    </div>   
    <div class="formClass"> 
        <form v-if="this.action!==''" @submit.prevent="sendRequest">
            <legend>{{ this.action }} Request</legend>
            <div v-if="this.action=='PUT'|| this.action=='DELETE'">
                <label for="c_id">Category ID </label>
                <input type="number" min="1" step="1" v-model="c_id" id="c_id">
            </div>
            <div v-if="this.action=='POST'|| this.action=='PUT'">
                <label for="c_name">Category Name: </label>
                <input id="c_name" type="text" v-model="c_name" >
            </div>
            <div v-if="this.action=='POST'|| this.action=='PUT'">
                <label for="c_image">Category Image: </label>
                <input id="c_image" type="file" accept="image/*">
            </div><br>
            <button type="submit" class="btn btn-outline-dark"
            data-bs-toggle="modal" data-bs-target="#requestForm">
                Send Request
            </button>
        </form>
    </div>
</template>
  
<script>
import {mapGetters} from 'vuex';

export default {
    name: 'RequestButton',
    data(){
        return {
            msg: 'Request Sent to Admin',
            action: '',
            c_name: '',
            c_id: null
        }
    },
    methods:{
        selectAction(action){
            if(this.action==action){ this.action='' }
            this.action=action
        },
        async sendRequest(){
            var formData = new FormData()
            const image = document.getElementById('c_image')
            if (image && image.files.length>0) {
                formData.append("c_image",image.files[0]);
            }
            if (this.c_name!=='') { formData.append('c_name',this.c_name); }
            if (this.c_id!==null){formData.append('c_id',this.c_id);}
            formData.append('action',this.action)
            
            try {
                const res = await fetch('http://10.0.2.15:8000/api/requests/create?auth_token='+this.GET_USER_TOKEN, {
                    method: 'POST',
                    body: formData,
                    mode: 'cors',
                    headers:{
                        'Access-Control-Allow-Origin': '*',
                    },
                    credentials: 'include'
                })
                const data = await res.json()
                if (!res.ok){ 
                    throw Error('HTTP Error at Send Category Request') }
                else if (res.status===202){
                    this.msg = data.message
                }else{
                    this.msg = 'Request Sent to Admin'
                }
            }catch(error){console.log(error.message)}
        }
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_TOKEN']),
    }
}
</script>

<style scoped>  
    label, select {
        width:150px;
    }
    form{
        border: 2px solid;
        padding: 20px;
        background-color: #d7f5c4;
    }  
    .formClass{
        padding-left: 80px;
        padding-right: 80px;
    }

</style>
  