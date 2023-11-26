<template>
    <div class="container d-flex justify-content-center">
        <div class="col-md-3"></div>
        <div class="col-md-6">
            <form class="h-100">
                <legend>Login</legend>
                <div class="row mb-3">
                    <label for="email" class="col-sm-3 col-form-label">Email</label>
                    <div class="col-sm-9">
                        <input type="email" class="form-control" id="email">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="password" class="col-sm-3 col-form-label">Password</label>
                    <div class="col-sm-9">
                        <input type="password" class="form-control" id="password">
                    </div>
                </div>
                <button type="submit" class="btn btn-success ">Login</button>
            </form>
        </div>
        <div class="col-md-3"></div>
    </div>
</template>

<script>
export default {
    name: 'Login'
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