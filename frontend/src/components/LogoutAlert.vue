<template>
    <!-- Button trigger modal -->
    <a href="#" class="nav-link" data-bs-toggle="modal" data-bs-target="#modal" 
    @click="logoutUser">Logout</a>

    <!-- Modal -->
    <div class="modal fade" id="modal" tabindex="-1" aria-labelledby="modallabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modallabel">{{ this.title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import {emitter} from '../main.js'

export default{
    name: 'LogoutAlert',
    data(){
        return {
            title: ''
        }
    },
    methods:{
        async logoutUser(){
            fetch('http://10.0.2.15:8000/api/logout', {
                method: 'GET',
                credentials: 'include'
            })
            .then((res)=>{
                if(!res.ok) {throw Error('HTTP error at Logout:'+res.status);}
                return res.json()
            }).then((data)=>{
                this.title = data.message;
                localStorage.setItem('user',JSON.stringify({roll:null}));
                this.refresh();
                emitter.emit('isLoggedIn', false);
                /* console.log('emit successful1'); */
            }).catch((error)=>console.log(error.message))
        },
        refresh(){
            const router = this.$router
            router.push('/login')
        }
    }
}
</script>