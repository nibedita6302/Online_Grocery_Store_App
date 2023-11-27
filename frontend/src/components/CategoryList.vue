
<template>
    <div id='top' class="row g-2">
        <div v-for="c in categories" class="col-4">
            <div v-if="c.product_count>0" class="card bg-dark text-white h-100"  >
                <img :src="get_url(c.c_image)" class="card-img-top" :alt="c.c_image">
                <div class="card-img-overlay">
                    <h3 class="card-title stretched-link" @click="categoryShow(c.c_id)">
                        {{ c.c_name }}
                    </h3>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CategoryList',
    data() {
        return {
            categories: []
        }
    },
    methods:{
        get_url(img){
            return require('@/assets/upload/'+img); 
        },
        categoryShow(c_id){
            console.log('here')
            this.$emit('showProducts',c_id);
        },
        async getAllCategory(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/category');
                if (!res.ok) {
                    throw Error("HTTP Error in CategoryList: "+ res.status);
                }
                const data = await res.json();
                this.categories = data;
            }catch(error) {
                console.log(error);
            }
            return null;
        }
    },
    mounted() { 
        this.getAllCategory();

    }
}
</script>

<style scoped>
    #top {
        padding: 40px;
    }
    h3{
        text-align: center;
    }
</style>
  
 
