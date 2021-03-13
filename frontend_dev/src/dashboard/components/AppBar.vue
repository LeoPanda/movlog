<template>
  <!--アプリケーショントップバー-->
  <v-app-bar id="app-bar" absolute app color="transparent" flat height="75">
    <v-app-bar-nav-icon class="pl-0">
      <!--ドロワー表示ボタン-->
      <v-btn class="mr-3" elevation="1" small @click="setDrawer(!drawer)">
        <v-icon v-if="drawer"> mdi-dots-vertical </v-icon>
        <v-icon v-else> mdi-view-quilt </v-icon>
      </v-btn>
    </v-app-bar-nav-icon>
    <!--バックボタン-->
    <v-btn class="mrl-3" elevation="1" fab x-small @click="goBack">
      <v-icon> mdi-arrow-left </v-icon>
    </v-btn>
    <v-spacer />
    <!--メインパネルのアプリ名-->
    <v-toolbar-title
      class="hidden-sm-and-down font-weight-light ml-3"
      v-text="$route.name"
    />
    <v-spacer />
    <!--表示件数-->
    <v-chip outlined class="ma-1" small v-if="isView">
      <v-icon class="d-flex justify-center mr-2" small>{{ eventsNum }}</v-icon>
    </v-chip>
    <div class="mx-1" />
    <!--表示順変更セレクタ-->
    <div
      class="mt-5"
      v-if="this.$route.path.match('/views/')"
      style="width: 50px"
    >
      <v-select
        append-icon=""
        dense
        solo
        :value="this.$store.state.sortOrder"
        :items="orderItems"
        @change="(value) => this.setSortOrder(value)"
      >
        <!--選択アイテムアイコン表示-->
        <template v-slot:selection="{ item }">
          <v-icon dense>{{ item.icon }}</v-icon>
        </template>
        <!--セレクタアイコン表示-->
        <template v-slot:item="{ item }">
          <v-list item-avatar>
            <v-icon dense>{{ item.icon }}</v-icon>
          </v-list>
        </template>
      </v-select>
    </div>
    <div class="mx-1" />

    <!--検索パネル-->
    <FilterSection />
    <div class="mx-3" />
    <!--データ変更通知ベル-->
    <InfoBell v-if="uploadItems.length" />
  </v-app-bar>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { setSortOrder } from "@/js/sort";
export default {
  name: "DashboardCoreAppBar",
  components: {
    FilterSection: () => import("./parts/FilterSection"),
    InfoBell: () => import("./parts/InfoBell"),
  },
  data() {
    return {
      //表示順制御アイテム
      orderItems: [
        { value: "dateDsc", icon: "mdi-sort-calendar-descending" },
        { value: "dateAsc", icon: "mdi-sort-calendar-ascending" },
        { value: "rateDsc", icon: "mdi-star-outline" },
      ],
    };
  },
  computed: {
    ...mapState(["drawer", "uploadItems", "eventsNum"]),
    isView() {
      return this.$route.path.match("views");
    },
  },

  methods: {
    //ドロワーのセット
    ...mapMutations({
      setDrawer: "SET_DRAWER",
    }),
    goBack() {
      //戻る
      this.$router.go(-1);
    },
    //ソート順変更をセット
    setSortOrder,
  },
};
</script>
<style scoped>
.v-btn:before {
  display: none;
}
</style>