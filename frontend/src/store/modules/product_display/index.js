export default ({
  namespaced: true,
  state() {
    return {
      onClickCategory: false,
      productList: [],
      c_id: null,
      p_review: null
    };
  },
  getters: {
    GET_PRODUCT_LIST(state){
      return state.productList
    },
    GET_CATEGORY_ID(state){
      return state.c_id;
    }
  },
  mutations: {
    STORE_PRODUCT_LIST(state, payload){
      state.productList = payload.productList;
      state.onClickCategory = true
      // console.log('category-products',state.productList, state.onClickCategory);
    },
    TOGGLE_ONCLICK_CATEGORY(state, payload){
      state.onClickCategory = payload.setTo;
      state.productList = [];
      state.c_id = null;
      // console.log(state.onClickCategory)
    },
    SET_CATEGORY_ID(state, payload){
      state.c_id = payload.c_id;
    },
    SET_REVIEW_P_ID(state,payload){
      state.p_review = payload.p_id;
    }
  },
  actions: {
  }
})
    