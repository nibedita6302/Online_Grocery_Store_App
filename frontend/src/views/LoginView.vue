
<template>
    <div class="container">
        <Login />
        <hr>
        <div class="container d-flex justify-content-center">
            <Register title="New Customer Register" button_msg="Register" 
            button_type="btn btn-warning" role="customer"/>
            <div class="spacer"></div>
            <Register title="Store Manager Register" button_msg="Apply for Approval"
            button_type="btn btn-danger" role="store_manager"/>
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
    .spacer{
        padding-left: 10px;
        padding-right: 10px;
    }
</style>

