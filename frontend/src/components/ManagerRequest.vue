<template>
    <div  class="modal fade " id="formModal2" 
        tabindex="-1" aria-labelledby="formModal2Label" >
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

    <h2>Store Manager Approvals</h2>
    <table class="table table-striped text-center">
    <thead>
        <tr>
        <th scope="col">User ID</th>
        <th scope="col">Request Email</th>
        <th scope="col">Approval</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(row,index) in this.approvals ">
            <th scope="row">{{row.id}}</th>
            <td>{{row.email}}</td>
            <td>
                <button type="submit" class="btn btn-success btn-sm me-2" 
                @click="sendApprovals(1,row.id)"
                data-bs-toggle="modal" data-bs-target="#formModal2">
                    <svg id="out-btn" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-square-fill" viewBox="0 0 16 16">
                        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
                        <path d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425z"/>
                    </svg>
                    Approve
                </button>
                <button type="submit" class="btn btn-danger btn-sm" 
                @click="sendApprovals(0, row.id)"
                data-bs-toggle="modal" data-bs-target="#formModal2">
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
    <p v-if="this.approvals.length==0" class="text-center">No Requests yet!</p>
</template>
  
<script>
import {mapGetters} from 'vuex';

export default {
    name: 'RequestsView',
    data(){
        return {
            approvals: [],
            showButton: true,
            msg: ''
        }
    },
    components:{
    },
    methods:{
        async getManagerRequests(){
            await fetch('http://10.0.2.15:8000/api/admin/store-manager-approvals?auth_token='
                                                                        +this.GET_USER_TOKEN, {
                method: 'GET',
                credentials: 'include'
            }).then((res)=>{
                if (!res.ok){
                    throw Error('HTTP Error at Get requests:',res.status);
                }
                return res.json()
            }).then((data)=>{
                if (data.message) {this.msg = data.msg;}
                else {this.approvals = data}
            }).catch((error)=>{console.log(error);})
        },
        async sendApprovals(status,id){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/admin/store-manager-approvals/'
                            +id+'?auth_token='+this.GET_USER_TOKEN, {
                    method: 'POST',
                    mode: 'cors',
                    body: JSON.stringify({
                        approved: status
                    }),
                    headers: {
                        'Content-Type':'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    credentials: 'include'
                })
                if (!res.ok){
                    throw Error('HTTP Error at Send Approvals:',res.status);
                }
                const data = await res.json()
                this.msg = data.message;
                await this.getManagerRequests();
            }catch(error){console.log(error);}
        }
    },
    computed: {
        ...mapGetters('auth',['GET_USER_ROLE','GET_USER_TOKEN']),
    },
    mounted() {
        if (this.GET_USER_ROLE=='admin') {
            this.getManagerRequests();
        }
    }
}
</script>

<style scoped>
    h2{
        text-align: center;
    }
</style>
  