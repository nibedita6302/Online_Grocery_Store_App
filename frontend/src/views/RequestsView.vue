<template>
    <div class="container">
        <div class="row">
            <RequestCategory />
        </div>
        <br><hr><br>
        <div v-if="this.GET_USER_ROLE=='admin'" class="row">
            <ManagerRequest />
        </div>
        <div v-else class="row">
            <RequestButton />
        </div>
    </div>
</template>
  
<script>
import {mapGetters, mapMutations, mapState} from 'vuex';
import RequestCategory from '@/components/RequestCategory.vue';
import ManagerRequest from '@/components/ManagerRequest.vue';
import RequestButton from '@/components/RequestButton.vue';

export default {
    name: 'RequestsView',
    data(){
        return {
            requests: [],
            approvals: [],
            msg: ''
        }
    },
    components:{
        RequestCategory,
        ManagerRequest,
        RequestButton
    },
    methods:{
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_TOKEN']),
    }
}
</script>

<style scoped>
    .container{
        padding: 50px;
    }
</style>
  