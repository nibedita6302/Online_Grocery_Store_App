<template>
    <div class="p-3 text-center">
        <h2>My Order History</h2>
    </div>
    <div class="container p-3" v-for="order in this.Orders">
        <div class="card mb-3 border-dark h-100" >
            <div class="card-body">
                <div class="row">
                    <div class="col-sm-7"><h5 class="card-title"> Order ID: {{ order.t_id }}</h5></div>
                    <div class="col-sm-5"><p class="card-title"> Order Date: {{ order.bought_date.split(' ')[0] }}</p></div>
                </div>
                <table class="table table-striped text-center">
                    <thead>
                        <tr class="table-success">
                            <th> Product Name </th>
                            <th> Seller </th>
                            <th> Quantity </th>
                            <th> Price </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row,index) in order.products " >
                            <td> {{ row.p_name  }} </td>
                            <td> {{ row.brand }} </td>
                            <td> {{ row.bought_qty }} </td>
                            <td> ₹{{ row.paid }} </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row">
                    <div class="col-sm-7"><p class="card-text">Delivery Charges: ₹50.00</p></div>
                    <div class="col-sm-5">
                        <h5 class="card-title">Total Payment: ₹{{ order.total_price }} </h5> 
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
    name: 'OrdersView',
    data(){
        return {
            Orders: []
        }
    },
    methods:{
        async getOrders(){
            await fetch('http://10.0.2.15:8000/api/customer/'+
                        this.GET_USER_ID+'/transaction?auth_token='+this.GET_USER_TOKEN, {
                method: 'GET',
                mode: 'cors',
                headers:{
                    'Access-Control-Allow-Origin': '*'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at GET Offers:',res.status);
                }
                return res.json()
            }).then((data)=>{
                this.Orders = data;
                console.log(this.Orders)
            }).catch((error)=>{console.log(error);})
        }
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ID','GET_USER_TOKEN']),
    },
    mounted(){
        this.getOrders();
    }
}
</script>

<style scoped>

</style>
