<template>
    <div class="container">
        <div class="row justify-content-center">
            <ShoppingList />
        </div>
    </div>
</template>

<script>
import ShoppingList from '../components/ShoppingList.vue'
import {mapGetters} from 'vuex';

export default {
    name: 'MyCartView',
    data(){
        return {
        }
    },
    components:{
        ShoppingList,
    },
    methods:{
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE']),
    }
}
</script>

<style scoped>
    .container{
        padding: 20px;
    }

</style>
