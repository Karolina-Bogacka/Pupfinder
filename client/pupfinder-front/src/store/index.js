import axios from "axios";
import { createStore } from 'vuex';

const store =  createStore({
  state: {
    token: "",
    expiration: Date.now(),
    isBusy: false,
    error: ""
  },
  mutations: {
    setBusy: (state) => state.isBusy = true,
    clearBusy: (state) => state.isBusy = false,
    setError: (state, error) => state.error = error,
    clearError: (state) => state.error = "",
    setToken: (state, model) => {
      state.token = model.token;
      state.expiration = model.exp*1000;
    },
    clearToken: (state) => {
      state.token = "";
      state.expiration = Date.now();
    }
  },
  getters: {
    isAuthenticated: (state) => state.token.length > 0 && state.expiration > Date.now()
  },
  actions: {
    register({commit}, owner){
      return new Promise((resolve, reject) => {
        var owner_json = JSON.stringify(owner);
        axios({url: 'http://localhost:8000/api/owners/', data: owner_json, method: 'POST' , headers: {
            'Content-Type': 'application/json'}})
        .then(resp => {
        })
        .catch(err => {
          console.log(err);
        })
      })
    },}
})

export default store;
