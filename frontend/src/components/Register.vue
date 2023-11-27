
<template>
    <div class="col-md-5" id="form1">
        <form class="h-100">
            <legend>{{title}}</legend>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">Email</label>
                <div class="col-sm-9">
                    <input type="email" class="form-control" >
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" >
                </div>
            </div>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">Confirm Password</label>
                <div class="col-sm-9">
                    <input type="password" class="form-control" >
                </div>
            </div>
            <button type="submit" v-bind:class="button_type">{{button_msg}}</button>
        </form>
    </div>
</template>

<script>
export default {
    props: {
        title: String,
        button_msg: String,
        button_type: String
    },
    name: 'Register'
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
