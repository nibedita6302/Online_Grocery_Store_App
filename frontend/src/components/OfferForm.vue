<template>
    <p v-if="this.msg!==''" class="text-success">{{ this.msg }}</p>
    <div class="container justify-content-start">
        <form id="offer-form"  @submit.prevent="createOffer">
            <legend >Create New Offer:</legend>
            <div v-for="f in form_fields" class="mb-3">
                <label :for="f.id">{{ f.label }}:</label>
                <input v-if="f.type=='number'" :type="f.type" :id="f.id" :min="f.min" :step="f.step" 
                v-model="f.data" required/>
                <input v-else :type="f.type" :id="f.id" v-model="f.data" required/>
            </div>
            <button type="submit" class="btn btn-success" 
            @click="createOffer">Confirm</button>
        </form>
    </div>    
</template>      

<script>
import { mapGetters } from 'vuex';

export default{
    name: "OfferForm",
    data() {
        return {
            form_fields: [
                {label: 'Offer Name', type:'text', id:'o_name', maxlength:"50", data:''},
                {label: 'Offer Description', type:'text', id:'description', maxlength:"100", data:''},
                {label: 'Discount', type:'number', id:'discount', min:"1", step:"1", data:''},
                {label: 'Selling Price', type:'number', min:"0", step:"0.1", id:'price', data:''},
                {label: 'Validity Count', type:'number',  min:"1", step:"1", id:'use_count'},
            ],
            msg: '',
            category: []
        }
    },
    methods: {     
        async createOffer(){
            var formData = new FormData()
            for(let f in this.form_fields){
                if (this.form_fields[f].type!=='file') {
                    formData.append(this.form_fields[f].id,this.form_fields[f].data);
                }
            }
            await fetch('http://10.0.2.15:8000/api/offers-customer/create?auth_token='+
                                                                    this.GET_USER_TOKEN, {
                method: 'POST',
                body: formData,
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Create Product:'+res.status)
                }
                return res.json()
            }).then((data)=>{
                if (data!=null) {this.msg = 'Successfully Operation';}
            }).catch((error)=>console.log(error.message))
        }
    }, 
    computed: {
        ...mapGetters('auth',['GET_USER_TOKEN'])
    }
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
        background-color: #e0f7e6;
        text-align: left;
    }  
    label, select {
        width:150px;
    }
    .container{
        padding-left: 75px;
        padding-right: 75px;
    }
</style>