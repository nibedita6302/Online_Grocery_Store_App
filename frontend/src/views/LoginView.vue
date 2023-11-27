
<template>
    <div class="container">
        <Login />
        <hr>
        <div class="container d-flex justify-content-center">
            <Register id='register' title="New Customer Register" button_msg="Register" 
            button_type="btn btn-warning"/>
            <Register id='register' title="Store Manager Register" button_msg="Apply for Approval"
            button_type="btn btn-danger"/>
        </div>
    </div>
</template>

<script>
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

export default {
    name: 'LoginView',
    components: {
        Login,
        Register
    }
}
</script>

<style scoped>
    div.container {
        padding: 20px;
        text-align: center;
    }
    #register {
        padding-left: 10px;
        padding-right: 10px;
    }
</style>

