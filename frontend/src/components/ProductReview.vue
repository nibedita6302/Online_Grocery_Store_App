<template>
    <div  class="modal fade " id="formModal3" 
        tabindex="-1" aria-labelledby="formModal3Label" >
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
    <div id='top' class="row  g-2">
        <div class="card h-100" id="prodCard">
            <div class="card-body">
                <h1 class="card-title">{{ this.p.p_name }} Review Page</h1>
                <h3 class="card-text">Seller: {{ this.p.brand }}</h3>
                <h5 class="card-text">Description: {{this.p.p_description}} |
                        {{this.p.p_qty}} {{this.p.unit}} | ₹{{this.p.price}} </h5>
                <p v-if="this.p.stock_remaining>5" class="card-text" style="color:green;">In Stock</p>
                <p v-else-if="this.p.stock_remaining>0" class="card-text" style="color:red;">
                    Only few left! 
                </p>
                <p v-else class="card-text" style="color:red;">Out of Stock</p>
            </div>
        </div>
    </div>
    <div>
        <h2>Customer Reviews: </h2>
        <form @submit.prevent="postReview">
            <label for="rate">Rating: </label>
            <input type="number" min="1" max="5" step="1" v-model="rating" id="rate"/><br>
            <label for="typereview">Type your review here: </label><br>
            <textarea type="text" v-model="text" id="typereview" row="200" col="200"></textarea><br>
            <button class="btn btn-warning" type="submit" >Post Review</button>
        </form>
    </div>
    <div id='top' class="row g-2" v-for="r in this.review">
        <div class="card h-100">
            <div class="card-body">
                <b class="card-text">User: {{ r.email }}</b>
                <h5 class="card-text">Rating: {{ r.rating }}</h5>
                <em class="card-text">Review: {{r.review}}</em>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex';

export default {
    name: 'ProductReview',
    data() {
        return {
            p: [],
            msg: '',
            review: [],
            text: '',
            rating: null
        }
    },
    methods:{
        async getProductReview(){
            await fetch('http://10.0.2.15:8000/api/product/'+this.p_review+
                        '/review?auth_token='+this.GET_USER_TOKEN, {
                method: 'GET',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Delete Product:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.review = data;
            }).catch((error)=>{console.log(error);})

        },
        async postReview(){
            await fetch('http://10.0.2.15:8000/api/customer/product/'+
                        this.p_review+'/review?auth_token='+this.GET_USER_TOKEN, {
                method: 'POST',
                mode: 'cors',
                body: JSON.stringify({
                    'rating': this.rating,
                    'review': this.text
                }),
                headers:{
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Delete Product:',res.status);
                }
                return res.json()
            }).then((data)=>{
                if (data.message!==null) {this.msg = data;}
                this.getProductReview();
            }).catch((error)=>{console.log(error);})
        },
        async get_product_detail(){
            await fetch('http://10.0.2.15:8000/api/product/'+this.p_review+
                    '?auth_token='+this.GET_USER_TOKEN, {
                method: 'GET',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Get 1 Product:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.p = data;
                // console.log(this.p, this.p.p_image, 'HELOOO')
            }).catch((error)=>{console.log(error);})
        }
    },
    computed:{
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_ID', 'GET_USER_TOKEN']),
        ...mapState('product_display',['p_review'])
    },
    mounted(){
        // console.log('here', this.p_review)
        this.get_product_detail()
        // console.log('here')
        this.getProductReview()
    }

}
</script>

<style scoped>
    img {
        max-height: 150px;
        max-width: 200px;
    }
    #top {
        padding: 20px;
    }
    p{
        font-weight: bold;
        font-size: larger;
    }
    #prodCard{
        background-color: lightyellow;
    }
</style>
  
