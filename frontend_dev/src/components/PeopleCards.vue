<template>
  <div class="row mx-0 text-right">
    <v-expansion-panels multiple>
      <!-- キャスト一覧（カード表示） -->
      <v-expansion-panel @click="onExpantion">
        <v-expansion-panel-header>CAST</v-expansion-panel-header>
        <v-expansion-panel-content>
          <slot>
            <PersonCard :people="casts" />
          </slot>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <!-- スタッフ一覧（カード表示） -->
      <v-expansion-panel @click="onExpantion">
        <v-expansion-panel-header>STAFF</v-expansion-panel-header>
        <v-expansion-panel-content>
          <slot>
            <PersonCard :people="crews" />
          </slot>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <!--ローディング中オーバーレイ -->
      <v-overlay absolute :value="progress">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-expansion-panels>
    <!--詳細ボタン-->
    <v-btn
      fab
      x-small
      v-if="gotCredits == 'short'"
      color="success"
      class="ma-1"
      @click="getFullCredits"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>
<script>
import { ajaxGet } from "@/js/ajax.js";
export default {
  name: "PeopleCards",
  props: ["tmdb_id"],
  components: {
    PersonCard: () => import("./parts/PersonCard"),
  },
  data() {
    return {
      casts: [],
      crews: [],
      progress: false,
      gotCredits: "none",
    };
  },
  methods: {
    async getCredit(id, full = false) {
      //映画のクレジット情報を取得する
      this.progress = true;
      const queryUrl = "/scrap/tmdb/credit/" + id + (full ? "?full" : "");
      const response = await ajaxGet(queryUrl);
      this.progress = false;
      if (response.status == 200) {
        this.casts = response.data["casts"];
        this.crews = response.data["crews"];
        this.gotCredits = full ? "full" : "short";
      }
    },
    onExpantion() {
      //expantionパネルを開いた時のアクション
      if (this.casts.length == 0) {
        this.getCredit(this.tmdb_id);
        this.shortCredited = true;
      }
    },
    getFullCredits() {
      //クレジット情報を全件取得する
      this.getCredit(this.tmdb_id, true);
    },
  },
};
</script>
