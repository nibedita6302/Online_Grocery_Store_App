import { createStore } from "vuex";
import auth from "./modules/auth/index";
import searching from "./modules/searching/index";
import product_display from "./modules/product_display/index";

const store = createStore({
    modules: {
        auth,
        searching,
        product_display
    }
})

const savedAuthData = localStorage.getItem('savedAuthData');

if (savedAuthData) {
    store.state.auth = JSON.parse(savedAuthData);
}

export default store;