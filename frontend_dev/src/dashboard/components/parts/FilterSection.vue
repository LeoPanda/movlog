<template>
  <!--検索パネル-->
  <!--検索ワード入力-->
  <v-text-field
    color="secondary"
    hide-details
    ref="search"
    style="max-width: 180px"
    v-model="word"
    @input="doFilter"
  >
    <!--検索ワード消去ボタン-->
    <template v-if="$vuetify.breakpoint.mdAndUp" v-slot:append-outer>
      <v-btn class="mt-n2" elevation="1" fab small @click="clearWord">
        <v-icon>mdi-eraser</v-icon>
      </v-btn>
    </template>
  </v-text-field>
</template>
<script>
export default {
  name: "FilterSection",
  data() {
    return {
      word: "",
    };
  },
  computed: {
    getSearchWord() {
      return this.$store.state.searchWord;
    },
  },
  methods: {
    doFilter() {
      this.$store.commit("SET_SEARCH_WORD", this.word);
    },
    clearWord() {
      this.word = "";
      this.doFilter();
    },
  },
  watch: {
    getSearchWord: function (newVal, oldVal) {
      //プログラムでセットされた検索ワードをUIに
      this.word = newVal;
      //検索ワードが変更されたら一覧表示へ遷移する
      if (
        newVal != oldVal &&
        newVal.length > 0 &&
        !this.$route.path.match("/views/")
      ) {
        this.$store.commit("SET_PAGE_START_INDEX", 0);
        this.$router.push({ name: "Movie List(Cards)" });
      }
    },
  },
};
</script>