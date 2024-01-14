import { createStore } from "vuex";
import auth from "./modules/auth/index";

const store = createStore({
    modules: {
        auth,
    }
})

const savedAuthData = localStorage.getItem('savedAuthData');

if (savedAuthData) {
    store.state.auth = JSON.parse(savedAuthData);
}

export default store;