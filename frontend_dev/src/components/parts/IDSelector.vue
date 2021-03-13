<template>
  <!--映画データベースのIDセレクタ-->
  <v-row>
    <!--ID-->
    <v-col class="pr-0 mr-0">
      <v-text-field :label="label" v-model="id_value" dense />
    </v-col>
    <!-- 値適用ボタン(外部DBへ問い合わせて親画面へ値を適用させる) -->
    <v-col class="pl-0 ml-0 pr-0 mr-0">
      <v-btn class="ma-0 pa-0" elevation="1" fab x-small @click="adaptValue">
        <v-icon>mdi-arrow-collapse-up</v-icon>
      </v-btn>
    </v-col>
    <!-- 候補セレクタ -->
    <v-col class="pl-0 ml-0">
      <v-select
        dense
        @click="getSelect(site)"
        :items="items"
        @change="
          (val) => {
            this.id_value = val;
            this.adaptValue();
          }
        "
        :label="label"
        :no-data-text="no_data_text"
      >
        <!--セレクタ表示カスタマイズ -->
        <template v-slot:item="{ item }">
          <!--ポスターアート -->
          <v-list-item-avatar tile color="grey lighten-3">
            <v-img width="20" height="40" :src="item.img"></v-img>
          </v-list-item-avatar>
          <!--タイトル名-->
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item-content>
        </template>
      </v-select>
    </v-col>
  </v-row>
</template>
<script>
import { ajaxGet } from "@/js/ajax.js";
export default {
  name: "IDSelector",
  props: ["keyword", "label", "site", "id"],
  data() {
    return { items: [], id_value: "", no_data_text: "" };
  },
  methods: {
    async getSelect(site) {
      //サーバーへ問い合わせてセレクタの表示アイテムを構成する
      this.no_data_text = "問い合わせ中..";
      const response = await ajaxGet(
        "/scrap/" + site + "/search/" + encodeURI(this.keyword)
      );
      this.no_data_text = "該当データなし";
      this.items = response.data.map((item) => {
        return { text: item.title, value: item.id, img: item.img_src };
      });
    },
    adaptValue() {
      //親画面へIDを返す
      this.$emit("input", this.id_value);
    },
  },
  mounted() {
    this.id_value = this.id;
  },
};
</script>
<style>
.v-select__slot {
  max-width: 490px;
}
.v-select__selection {
  max-width: 172px;
}
</style>