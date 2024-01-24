<template>
    <OfferList />
</template>

<script>
import OfferList from '@/components/OfferList.vue';
import {mapGetters, mapMutations, mapState} from 'vuex';

export default {
    name: 'OfferView',
    data(){
        return {
        }
    },
    components:{
        OfferList
    },
    methods:{
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE']),
    }
}
</script>

<style scoped>

</style>
  