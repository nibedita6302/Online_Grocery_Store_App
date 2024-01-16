export default ({
    namespaced: true,
    state() {
      return {
        data: null
      };
    },
    getters: {
      GET_FORM_DATA(state){
        return state.data
      }
    },
    mutations: {
      STORE_FORM_DATA(state, payload){
        state.data = payload.data;
        // console.log(state.data)
      }
    },
    actions: {
    }
  })
    