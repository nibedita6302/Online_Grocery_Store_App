import Home from "./components/Home.js"
import Login from "./components/Login.js"

const routes = [
    {path: '/', component: Home},
    {path: '/login', component: Login},
]

export default new VueRouter({
    routes,
})