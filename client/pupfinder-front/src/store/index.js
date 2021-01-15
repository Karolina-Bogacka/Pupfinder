import router from "../router.js";
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
    },
    login: async ({ commit }, model) => {
      /*try {
        var report = JSON.stringify(model);
        //const result = await axios.post('http://localhost:8000/api/auth/token', report);
        var response = await client(axios.create(), {
          url: 'http://localhost:8000/api/auth/token',
          method: 'post',
          grant_type: "authorization_code",
          client_id: 'foo',
          client_secret: 'bar',
        });

        console.log(response);
        const result = await axios.request({
          url: "http://localhost:8000/api/auth/token",
          method: "post",
          auth: model,
          data: {
            "grant_type": "client_credentials"
            }
        })
        console.log(result);
        if (result.data) {
          commit("setToken", result.data.access_token);
          router.push("/");
        }
        else {
          commit("setError", "Authentication Failed");
        }
      } catch {
        commit("setError", "Failed to login");
      } finally {
        commit("clearBusy");
      }
    },
    logout: ({ commit }) => {
      commit("clearToken");
      router.push("/");
    }*/
  }}
})

export default store;
