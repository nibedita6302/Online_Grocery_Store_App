import { createStore } from "vuex";
import auth from "./modules/auth/index";
import searching from "./modules/searching";

const store = createStore({
    modules: {
        auth,
        searching,
    }
})

const savedAuthData = localStorage.getItem('savedAuthData');

if (savedAuthData) {
    store.state.auth = JSON.parse(savedAuthData);
}

export default store;