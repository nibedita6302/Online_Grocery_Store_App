<template>
    <!-- ALERT MESSAGE GIVING ERROR! -->
    <h2>Request On Category</h2>
    <p :class="msg_type">{{ this.msg }}</p>
    <table class="table text-center">
    <thead>
        <tr>
        <th scope="col">Request ID</th>
        <th scope="col">Request Date</th>
        <th scope="col">Action</th>
        <th scope="col">Category ID</th>
        <th scope="col">Category Name</th>
        <th scope="col">Image</th>
        <th v-if="this.GET_USER_ROLE=='store_manager'" scope="col">Status</th>
        <th v-if="this.GET_USER_ROLE=='admin'" scope="col">Approval</th>        
        </tr>
    </thead>
    <tbody>
        <tr v-for="(row,index) in this.requests " :class="getColor(row.action)">
            <th scope="row">{{row.cn_id}}</th>
            <td>{{row.req_date.split(' ')[0]}}</td>
            <td>{{row.action}}</td>
            <td v-if="row.c_id!==0">{{row.c_id}}</td> <td v-else>N/A</td>
            <td v-if="row.c_name!==''">{{row.c_name}}</td> <td v-else>N/A</td>
            <td v-if="row.c_image!==''">{{row.c_image}}</td> <td v-else>N/A</td>
            <td v-if="this.GET_USER_ROLE=='store_manager'"> {{ this.printStatus(row.status) }} </td>
            <td v-if="this.GET_USER_ROLE=='admin'">
                <button type="submit" class="btn btn-success btn-sm me-2" 
                @click="returnRequest(1,row.cn_id)">
                    <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-square-fill" viewBox="0 0 16 16">
                        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                        <path d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>
                    </svg>
                    Approve
                </button>
                <button type="submit" class="btn btn-danger btn-sm" 
                @click="returnRequest(0, row.cn_id)">
                    <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-square" viewBox="0 0 16 16">
                        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                    </svg>
                    Deny
                </button>
            </td>
        </tr>
    </tbody>
    </table>
    <p v-if="this.requests.length==0" class="text-center">No Requests yet!</p>
</template>
  
<script>
import {mapGetters} from 'vuex';

export default {
    name: 'RequestCategory',
    data(){
        return {
            requests: [],
            msg: '',
            msg_type: 'text-success'
        }
    },
    components:{
    },
    methods:{
        getColor(action){
            if (action=='POST'){ return 'table-warning' }
            else if (action=='PUT') { return 'table-info' }
            else { return 'table-danger' }
        },
        printStatus(status){
            if (status===-1){
                return 'Pending'
            }else if (status===0){
                return 'Rejected'
            }else { return 'Accepted' }
        },
        async getRequests(){
            await fetch('http://10.0.2.15:8000/api/requests?auth_token='+this.GET_USER_TOKEN, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Content-Type':'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Get requests:',res.status);
                }
                return res.json()
            }).then((data)=>{
                if (data.message) {this.msg = data.msg;}
                else {this.requests = data}
                // console.log(data)
            }).catch((error)=>{console.log(error);})
        },
        async returnRequest(status, cn_id){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/admin/requests/'+
                            cn_id+'?auth_token='+this.GET_USER_TOKEN, {
                    method: 'PUT',
                    mode: 'cors',
                    body: JSON.stringify({
                        status: status
                    }),
                    headers: {
                        'Content-Type':'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    credentials: 'include'
                })    
                if (res.status==202){
                    this.msg_type='text-danger'
                }else if (res.status==200){
                    this.msg_type='text-success'
                }
                if (!res.ok){ throw Error('HTTP Error at Return requests:'+res.status); }
                const data = await res.json()
                console.log(data)
                if (data!==null) {this.msg = data.message;}
                await this.getRequests()
                // console.log('here')
            }catch(error){console.log(error);}
        }
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_TOKEN']),
    },
    mounted() {
        this.getRequests();
    }
}
</script>

<style scoped>
    h2,p{
        text-align: center;
    }
</style>
  