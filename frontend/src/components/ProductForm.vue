<template>
    <div  class="modal fade " id="formModal2" 
        tabindex="-1" aria-labelledby="formModal2Label" >
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
    <div class="container">
        <form id="prod-form"  @submit.prevent="selectApi">
            <legend v-if="this.GET_FORM_DATA!=null">
                Update Product: {{this.GET_FORM_DATA.p_name}}
            </legend>
            <legend v-else >Create Product</legend>
            <div v-for="f in form_fields" class="mb-3">
                <label :for="f.id">{{ f.label }}:</label>
                <input v-if="f.type=='file'" :type="f.type" :id="f.id" accept="image/*" 
                :required="isRequired" v-model="f.data">
                <input v-else-if="f.type=='number'" :type="f.type" :id="f.id" :min="f.min" :step="f.step" 
                :placeholder="placeholder(f.id)" 
                :required="isRequired" v-model="f.data"/>
                <select v-else-if="f.type=='select'" :id="f.id"  v-model="f.data" 
                :required="isRequired" >
                    <!-- CACHE CATEGORIES -->
                    <option v-for="c in category" name="{{c.c_id}}" :value="c.c_id" :key="c.c_id">
                        {{ c.c_name }}
                    </option>
                </select>
                <input v-else :type="f.type" :id="f.id" :maxlength="f.maxlength" 
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
    name: "ProductForm",
    props: ['action'],
    data() {
        return {
            form_fields: [
                {label: 'Product Name', type:'text', id:'p_name', maxlength:"50", data:''},
                {label: 'Product Description', type:'text', id:'p_description', maxlength:"100", data:''},
                {label: 'Product Image', type:'file', id:'p_image'},
                {label: 'Select a Category', type:'select', id:'c_id', data:''},
                {label: 'Price per unit (₹)', type:'number', min:"1", step:"0.01", id:'price', data:''},
                {label: 'Quantity per unit', type:'number',  min:"1", step:"1", id:'p_qty'},
                {label: 'Units (Eg: Kg, L)', type:'text', id:'unit', maxlength:"10", data:''},
                {label: 'Total Stock', type:'number',  min:"1", step:"1", id:'stock'},
                {label: 'Seller', type:'text', id:'brand', maxlength:"20", data:''}
            ],
            msg: 'Something',
            category: []
        }
    },
    methods: {
        placeholder(id){
            if (this.GET_FORM_DATA!=null){
                return this.GET_FORM_DATA[id]
            } return ' '
        },
        isRequired(){
            if (this.$props.action=='POST'){ return true } 
            else {return false}
        },
        selectApi(){
            var formData = new FormData()
            const image = document.getElementById('p_image')
            if (image && image.files.length>0) {
                formData.append("p_image",image.files[0]);
            }
            for(let f in this.form_fields){
                if (this.form_fields[f].type!=='file') {
                    formData.append(this.form_fields[f].id,this.form_fields[f].data);
                }
            }
            if (this.$props.action=='PUT'){
                // console.log('called update');
                this.updateProduct(formData);
            }else{ 
                this.createProduct(formData); // action = POST 
            }
        },
        async updateProduct(newData){
            /* console.log('start')
            for (var key of newData.entries()){
                console.log(key[0]+" "+key[1])
            } */
            await fetch('http://10.0.2.15:8000/api/product/'+this.GET_FORM_DATA.p_id+
                    '/edit?auth_token='+this.GET_USER_TOKEN, {
                method: 'PUT',
                body: newData,
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                return res.json()
            }).then((data)=>{
                if (data!=null) {this.msg = "Product Updated!";}
            }).catch((error)=>console.log(error.message))
        },
        async createProduct(newData){
            await fetch('http://10.0.2.15:8000/api/product/create?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                body: newData,
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
                if (data!=null) {this.msg = data.message;}
            }).catch((error)=>console.log(error.message))

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
                this.category = data;
            }catch(error) {
                console.log(error);
            }
            return null;
        },
    }, 
    computed: {
        ...mapGetters('formdata',['GET_FORM_DATA']),
        ...mapGetters('auth',['GET_USER_TOKEN'])
    },
    mounted(){
        this.getAllCategory();
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
        background-color: #d7f5c4;
    }  
    label, select {
        width:150px;
    }
</style>