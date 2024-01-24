<template>
    <!-- CONFIRM MODAL -->
    <div  class="modal fade " id="Confirm" 
        tabindex="-1" aria-labelledby="ConfirmLabel" >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-body ">
                    <p v-if="this.delete===true">Please click Confirm if you want to DELETE Offer</p>
                    <p v-else>Please click Confirm to proceed to payment!</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-bs-dismiss="modal"
                    data-bs-toggle="modal" data-bs-target="#offerAlert"  
                    @click="()=>{
                            if (this.delete===true) {this.deleteOffer(this.store_offer_id);}
                            else {this.buyOffer(this.store_offer_id);}
                            this.delete=false; }" >
                    Confirm
                    </button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <!-- ALERT MODAL -->
    <div  class="modal fade " id="offerAlert" 
        tabindex="-1" aria-labelledby="offerAlertLabel" >
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

    <div class="text-center p-3" v-show="this.GET_USER_ROLE=='admin'">
        <button type="submit" class="btn btn-outline-success border-4 me-4" 
        @click="()=>{this.show_offer_update_form=!this.show_offer_update_form}">
            <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>
            Create Offer
        </button> <hr>
        <OfferForm v-if="this.show_offer_update_form"/>
    </div>

    <div id='top' class="container">
        <div class="row g-2">
        <div v-for="offer in this.offerList" class="col-6">
            <div class="card h-100 text-center">
                <img :src="get_url('offer_background.jpeg')" class="card-img" >
                <div class="card-img-overlay">
                    <div class="card-header">
                        <h3>{{ offer.o_name }}</h3>
                    </div>
                    <div class="card-body">
                        <em class="card-title">
                            Get Discount of {{ offer.discount }}% for {{ offer.use_count }} consecutive
                            purchase! Only for ₹{{ offer.price }}. Hurry Up, Buy Now!!
                        </em>
                    </div>
                    <div class="card-body">
                        <p class="card-text"> {{ offer.description }} </p>
                    </div>
                    <div class="card-footer">
                        <div v-if="this.GET_USER_ROLE=='customer'">
                            <button type="submit" class="btn btn-outline-dark me-2" 
                            data-bs-toggle="modal" data-bs-target="#Confirm"
                            @click="()=>{this.store_offer_id=offer.o_id}">
                            Buy Now</button>
                        </div>
                        <div v-if="this.GET_USER_ROLE=='admin' && offer.o_id!==1">
                            <button type="submit" class="btn btn-danger" 
                            data-bs-toggle="modal" data-bs-target="#Confirm"
                            @click="()=>{this.store_offer_id=offer.o_id; this.delete=true;}">
                                <svg id="in-btn" xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                                    <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/>
                                </svg>
                            Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
import OfferForm from './OfferForm.vue';
import { mapGetters } from 'vuex';

export default {
    name: 'OfferList',
    data() {
        return {
            offerList: [],
            show_offer_update_form: false,
            store_offer_id: null,
            action: null,
            msg: 'Operation Successful',
            delete: false
        }
    },
    components:{
        OfferForm,
    },
    methods:{
        get_url(img){
            return require('@/assets/'+img); 
        },
        async deleteOffer(o_id){
            await fetch('http://10.0.2.15:8000/api/offers-customer/'
                        +o_id+'/delete?auth_token='+this.GET_USER_TOKEN, {
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
        async get_offers(){
            await fetch('http://10.0.2.15:8000/api/offers-customer?auth_token='+this.GET_USER_TOKEN, {
                method: 'GET',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*',
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Get Offers:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.offerList = data
            }).catch((error)=>{console.log(error);})
        },
        async buyOffer(o_id){
            await fetch('http://10.0.2.15:8000/api/customer/buy-offer/'+
                        o_id+'?auth_token='+this.GET_USER_TOKEN, {
                method: 'PUT',
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
    },
    mounted(){
        this.get_offers();
    }
}
</script>

<style scoped>
    img {
        max-height: 300px;
        max-width: 600px;
    }
    #top {
        padding: 40px;
    }
    em {
        color: purple;
        font-size: large;
        font-weight: bold;
    }
    .card-footer{
        text-align: right;
    }
</style>
  
