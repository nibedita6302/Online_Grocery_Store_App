<template>
    <div  class="modal fade " id="formModal3" 
        tabindex="-1" aria-labelledby="formModal3Label" >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body ">
                    <p v-if="this.products.length<1">My Cart Empty!</p>
                    <p v-else>Click Confirm to proceed to payment</p>
                </div>
                <div class="modal-footer">
                    <button v-if="this.products.length>0" type="button" class="btn btn-success" 
                    data-bs-dismiss="modal" @click="purchase">
                        Confirm
                    </button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <div class="col-sm-6">
        <h1> My Shopping List </h1> <hr>
        <h5 v-if="this.products.length<1">My Cart is Empty, Hurry Up and buy something!! </h5>
        <div v-for="p in products">
            <div class="card mb-3">
            <div class="row g-0">
                <div class="col-md-4">
                    <img :src="get_url(p.p_image)" class="img-fluid rounded-start">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">{{ p.p_name }}</h5>
                        <em class="card-text">{{ p.brand }}</em>
                        <p class="card-text">{{p.p_description}} | {{p.p_qty}} {{p.unit}} | ₹{{p.price}} </p>
                        <p v-if="p.stock_remaining>5" class="card-text" style="color:green;">In Stock</p>
                        <p v-else-if="p.stock_remaining>0" class="card-text" style="color:red;">
                            Only few left! Remaining {{ p.stock_remaining }}
                        </p>
                        <p v-else class="card-text" style="color:red;">Out of Stock</p>
                    </div>
                </div>            
                <div class="card-footer"> 
                    <div>
                        <label for="totalQty">Quantity</label> 
                        <input type="number" id="totalQty" :placeholder="p.bought_qty" 
                        min="1" step="1" :max="p.stock_remaining" v-model="count"/>&nbsp;
                        <button class="btn btn-warning me-2" type="submit"
                        @click="editMyCart(p.p_id)">UPDATE</button>
                        <button class="btn btn-danger" type="submit"
                        @click="delete_from_MyCart(p.p_id)">DELETE</button>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
    <div class="col-sm-6">  
        <h1> Buy Now </h1> 
        <div class="card mb-3">
            <div class="row g-0">
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">Sub-Total: ₹{{ this.subtotal }}</h5>
                        <p class="card-text">Delivery Chargers: ₹50.00 </p>
                        <h5 class="card-title">Total Payment: ₹{{ this.subtotal + 50 }}</h5>
                        <button class="btn btn-warning " type="submit" 
                        data-bs-toggle="modal" data-bs-target="#formModal3">
                            BUY NOW
                        </button>
                    </div>
                    {{ this.offer_details }}
                    <div v-if="this.offer_details!==null" class="card-body">
                        <h5 class="card-title">Offer Applied: {{ this.offer_details.o_name }}</h5>
                        <p class="card-text">Discount: {{ this.offer_details.discount }}% </p>
                        <h5 class="card-title">Final Payment: ₹{{ this.offer_details.total_price }}</h5>
                        <em>Use Count Remaining: {{ this.offer_details.use_count_remaining }}</em>
                    </div>
                </div>
            </div> 
        </div>  <hr>
        <div v-if="this.msg!==''">
            <h5>Alert!</h5>
            <p>{{ this.msg }}</p>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';

export default {
    name: 'ShoppingList',
    data() {
        return {
            products: [],
            cart_id: null,
            msg: '',
            subtotal: 0.0,
            count: null,
            offer_details: null
        }
    },
    methods:{
        calculateSubtotal(){
            if (this.products.length>0){
                // console.log('in here',this.subtotal)
                for (let p in this.products){
                    this.subtotal+=this.products[p].bought_qty*this.products[p].price
                }
                // console.log(this.subtotal)
            }
        },
        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        selectApi(action,p_id){
            if (action=='PUT'){
                this.editMyCart(p_id)
            }else{
                this.delete_from_MyCart(p_id);
            }
        },
        async getProductList(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/customer/'+
                                        this.GET_USER_ID+'/mycart?auth_token='+this.GET_USER_TOKEN, {
                    method: 'GET',          
                    mode: 'cors',
                    headers:{
                        'Access-Control-Allow-Origin': '*',
                    },
                    credentials: 'include'
                });
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList - GetAll: "+ res.status);
                }
                const data = await res.json();
                this.products = data['products'];
                this.cart_id = data['cart_id'];
            }catch(error) {
                console.log(error);
            }
            return null;
        },
        async delete_from_MyCart(p_id){
            await fetch('http://10.0.2.15:8000/api/customer/mycart/delete/'+
                        p_id+'?auth_token='+this.GET_USER_TOKEN, {
                method: 'DELETE',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList - Delete: "+ res.status);
                }
                return res.json()
            }).then((data)=>{
                this.msg = data.message;
                // console.log(this.msg)
            }).catch((error)=>{console.log(error);})
        },
        async editMyCart(p_id){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/customer/mycart/update/'+
                                        p_id+'?auth_token='+this.GET_USER_TOKEN,{
                    method: 'PUT',
                    mode: 'cors',
                    body: JSON.stringify({'bought_qty':this.count}),
                    headers:{
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include'
                });
                if (!res.ok) {
                    throw Error("HTTP Error at ProductList: "+ res.status);
                }
                const data = await res.json();
                this.msg = 'Product Successfully Updated!'
            }catch(error) {
                console.log(error);
            }
        },
        async purchase(){
            await fetch('http://10.0.2.15:8000/api/customer/'+
                        this.GET_USER_ID+'/place-order?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList - Delete: "+ res.status);
                }
                return res.json()
            }).then((data)=>{
                this.msg = data.message;
                if (typeof data.offer=='undefined') {this.offer_details=null}
                else {this.offer_details = data.offer;}
                // console.log(this.msg)
            }).catch((error)=>{console.log(error);})
        }  
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ID','GET_USER_TOKEN']),
    },
    async mounted() { 
        await this.getProductList();
        // console.log('in mounted')
        this.calculateSubtotal();
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
  
 
