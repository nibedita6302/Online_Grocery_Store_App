<template>
    <div class="container d-flex justify-content-center">
        <div class="col-md-3"></div>
        <div class="col-md-6">
            <form class="h-100" @submit.prevent="loginUser">
                <legend>Login</legend>
                <div class="row mb-3">
                    <label for="email" class="col-sm-3 col-form-label" >Email</label>
                    <div class="col-sm-9">
                        <input type="email" class="form-control" id="email" v-model="email" />
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="password" class="col-sm-3 col-form-label">Password</label>
                    <div class="col-sm-9">
                        <input type="password" class="form-control" id="password" v-model="password" />
                    </div>
                </div>
                <button type="submit" class="btn btn-success" @click="loginUser">Login</button><hr>
                <p :class="this.msg_type" >{{ this.message }}</p>
            </form>
        </div>
        <div class="col-md-3"></div>
    </div>
</template>

<script>
export default { 
    name: 'Login',
    data(){
        return {
            email: '',
            password: '',
            message: '',
            msg_type: 'text-success'
        }
    },
    methods: {
        async loginUser(){
            try{
                const res = await fetch('http://10.0.2.15:8000/api/login', {
                    method: "POST",
                    headers: {
                        'Content-Type':'application/json'
                    },
                    body: JSON.stringify({
                        email:this.email,
                        password:this.password
                    })
                })
                const data = await res.json()
                if (res.status==401) {
                    this.message=data.message;
                    this.msg_type='text-danger';
                } else if(!res.ok){
                    throw Error('HTTP Error at Login:'+res.status);
                } else {
                    localStorage.setItem('user', JSON.stringify(data));
                    this.message=data.message;
                    this.msg_type='text-success';
                    this.emitter.emit('loginUser');
                }  
            }catch(error){console.log(error.message)} ;
        }
    }
}
</script>

<style scoped>
    form {
        border: 1px solid black;
        padding: 25px;    
    }
    legend {
        font-weight: 600;
        font-size: x-large;
        text-align: center;
    }
</style>
