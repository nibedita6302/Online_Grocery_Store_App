<template>
    <div class="col-md-5" id="form1">
        <form class="h-100 register-form" @submit.prevent="register">
            <legend>{{title}}</legend>
            <div class="row mb-3">
               <label class="col-sm-3 col-form-label">Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" v-model="this.email" >
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" v-model="this.password">
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">Confirm Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" v-model="this.confirm">
                </div>
            </div>

            <button type="submit" v-bind:class="button_type" @click="register">{{button_msg}}</button>
            <hr>
            <p :class="this.msg_type" >{{ this.msg }}</p>
        </form>
    </div>
</template>

<script>
export default {
    name: 'Register',
    props: {
        title: String,
        button_msg: String,
        button_type: String,
        role: String
    },
    data(){
        return {
            email: '',
            password: '',
            confirm: '',
            msg: '',
            msg_type: 'text-success'
        }
    },
    methods:{
        register(){
            if (this.password==''||this.email==''||this.confirm==''){
                this.msg = 'All field are compulsory!'
                this.msg_type = 'text-danger'
            }
            else if (this.password!=this.confirm){
                this.msg = 'Confirm Password not matching'
                this.msg_type = 'text-danger'
            }else if (this.$props.role=='customer'){
                this.userRegister('customer');
            }else{
                this.userRegister('store-manager');
            }
        },
        async userRegister(url){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/'+url+'/register', {
                    method: 'POST',
                    mode: 'cors',
                    headers: {
                        'Content-Type':'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    body: JSON.stringify({
                        email:this.email,
                        password:this.password
                    }),
                    credentials: 'include'
                })
                const data = await res.json()
                if (res.status==202) {
                    if (data!==null){
                        this.msg=data.message;
                        this.msg_type='text-danger';
                    }
                }else if(!res.ok){
                    throw Error('HTTP Error at User Registration', res.status)
                }else{
                    if (data!==null){
                        this.msg=data.message;
                        this.msg_type='text-success';
                    }
                }
            }catch(error){console.log(error.message)} ;
        }
    }
}
</script>

<style scoped>
    .register-form{
        border: 1px solid black;
        padding: 25px;
    }
    legend {
        font-weight: 600;
        font-size: x-large;
        text-align: center;
    }   
</style>
