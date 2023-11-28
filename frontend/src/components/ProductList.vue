
<template>
    <div id='top' class="row row-cols-1 row-cols-md-3 g-2">
        <div v-for="p in products" class="col-3">
            <div class="card h-100">
                <img :src="get_url(p.p_image)" class="card-img-top" :alt="p.p_image">
                <div class="card-body">
                    <h5 class="card-title">{{ p.p_name }}</h5>
                    <em class="card-text">{{ p.brand }}</em>
                    <p class="card-text">{{p.p_description}} | {{p.p_qty}} {{p.unit}} | ₹{{p.price}} </p>
                    <p v-if="p.stock_remaining>5" class="card-text" style="color:green;">In Stock</p>
                    <p v-else-if="p.stock_remaining>0" class="card-text" style="color:red;">
                        Only few left!
                    </p>
                    <p v-else class="card-text" style="color:red;">Out of Stock</p>
                    <form>
                        <input type="number" value="1" min="1" :max="p.stock_remaining" required/>
                        <button class="btn btn-warning" @click="addToCart" :disabled="p.stock_remaining==0">
                            Add to Cart
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['c_id'],
    name: 'ProductList',
    data() {
        return {
            products: []
        }
    },
    methods:{
        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        listenSearch(products) {
            // console.log('here')
            this.products = products;
            this.emitter.off("searchProducts", this.listenSearch);
        },
        addToCart(){

        }
    },
    watch: {
        c_id: async function(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/product/category/'+this.c_id);
                if (!res.ok) {
                    throw Error("HTTP Error: "+ res.message+" "+ res.status);
                }
                const data = await res.json();
                console.log(data);
                this.products = data;
            }catch(error) {
                console.log(error);
            }
            return null;
        }
    },
    mounted() {
        this.emitter.on("searchProducts", this.listenSearch);
    }
}
</script>

<style scoped>
    img {
        max-height: 150px;
        max-width: 200px;
    }
    #top {
        padding: 40px;
    }
</style>
  
