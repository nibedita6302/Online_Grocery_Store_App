
<template>
    <div id='top' class="row row-cols-1 row-cols-md-2 g-4">
        <div v-for="p in products" class="col-3">
            <div class="card">
                <img :src="get_url(p.p_image)" class="card-img-top" :alt="p.p_image">
                <div class="card-body">
                    <h5 class="card-title">{{ p.p_name }}</h5>
                    <p class="card-text">{{p.p_description}} | {{p.p_qty}} {{p.unit}} | ₹{{p.price}} </p>
                    <p v-if="p.stock_remaining>5" class="card-text" style="color:green;">In Stock</p>
                    <p v-else-if="p.stock_remaining>0" class="card-text" style="color:red;">
                        Only few left!
                    </p>
                    <p v-else class="card-text" style="color:red;">Out of Stock</p>
                    <form>
                        <input type="number" value="1" min="1" :max="p.stock_remaining" required/>
                        <button class="btn btn-warning" :disabled="p.stock_remaining==0">
                            Add to Cart
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { computed } from '@vue/reactivity';

export default {
    name: 'ProductList',
    data() {
        return {
            products: [
            {
                p_name: "Milk",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 2,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            },
            {
                p_name: "Paneer",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 0,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            },
            {
                p_name: "Ghee",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 10,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            },
            {
                p_name: "Milk",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 10,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            },
            {
                p_name: "Paneer",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 10,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            },
            {
                p_name: "Ghee",
                p_description: "Healthy Milk for Immunity",
                p_qty: 500,
                unit: "mL",
                price: 23.5,
                stock_remaining: 10,
                p_image: "milk.jpeg",
                expieryDate: "2023-11-20",
                c_id: 1,
                b_id: 1
            }
            ]
        }
    },
    methods:{
        get_url(img){
            return require('@/assets/upload/'+img); 
        }
    }
}
</script>

<style scoped>
    img {
        max-height: 120px;
        max-width: 120px;
    }
    #top {
        padding: 10px;
    }
</style>
  
