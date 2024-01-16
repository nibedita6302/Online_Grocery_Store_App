import { createStore } from "vuex";
import auth from "./modules/auth/index";
import searching from "./modules/searching/index";
import product_display from "./modules/product_display/index";
import formdata from "./modules/formdata";

const store = createStore({
    modules: {
        auth,
        searching,
        product_display,
        formdata
    }
})

const savedAuthData = localStorage.getItem('savedAuthData');

if (savedAuthData) {
    store.state.auth = JSON.parse(savedAuthData);
}

export default store;