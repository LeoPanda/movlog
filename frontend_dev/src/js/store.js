import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    drawer: null,
    searchWord: "",
    sortOrder: "",
    events: [],
    userInfo: {},
    locations: [],
    tables: {},
    uploadItems: [],
    pageStartIndex: 1,
    eventsNum: 0,
    loading: false,
    message: {},
  },
  mutations: {
    SET_DRAWER(state, payload) {
      state.drawer = payload
    },
    SET_EVENTS(state, payload) {
      state.events = payload
    },
    SET_USER_INFO(state, payload) {
      state.userInfo = payload
    },
    SET_LOCATIONS(state, payload) {
      state.locations = payload
    },
    SET_SEARCH_WORD(state, payload) {
      state.searchWord = payload
    },
    SET_SORT_ORDER(state, payload) {
      state.sortOrder = payload
    },
    SET_PAGE_START_INDEX(state, payload) {
      state.pageStartIndex = payload
    },
    SET_EVENTS_NUM(state, payload) {
      state.eventsNum = payload
    },
    SET_LOADING(state, payload) {
      state.loading = payload
    },
    SET_TABLES(state, payload) {
      state.tables = payload
    },
    SET_UPLAD_ITEMS(state, payload) {
      state.uploadItems = payload
    },
    SET_MESSAGE(state, payload) {
      state.message = payload
    }
  },
  actions: {

  },
})
