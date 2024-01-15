export default ({
  namespaced: true,
  state() {
    return {
      showProducts: false,
      searchOutput: []
    };
  },
  getters: {
    GET_SEARCH_OUTPUT(state){
      return state.searchOutput
    }
  },
  mutations: {
    STORE_SEARCH_PRODUCTS(state, payload){
      state.searchOutput = payload.searchOutput;
      state.showProducts = true
      console.log(state.searchOutput, state.showProducts);
    },
    TOGGLE_SEARCH_OUTPUT(state, payload){
      state.showProducts = payload.setTo;
      console.log(state.showProducts)
    }
  },
  actions: {
  }
})
  