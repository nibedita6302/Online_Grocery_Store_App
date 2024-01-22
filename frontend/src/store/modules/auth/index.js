export default ({
  namespaced: true,
  state() {
    return {
      id: null,
      role: '',
      token: null
    };
  },
  getters: {
    GET_USER_ID(state){
      return state.id
    },
    GET_USER_ROLE(state){
      return state.role
    },
    GET_USER_TOKEN(state){
      return state.token
    }
  },
  mutations: {
    SET_LOGIN_USER_DATA(state, payload){
      state.id = payload.id,
      state.role = payload.role,
      state.token = payload.token
    },
    REMOVE_LOGOUT_USER_DATA(state){
      state.id = null,
      state.role = '',
      state.token = null
    }
  },
  actions: {
    
  }
})
