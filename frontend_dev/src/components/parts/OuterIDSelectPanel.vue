<template>
  <!--映画データベース検索コンポーネント-->
  <v-card width="100%" class="mx-3">
    <v-row>
      <!--外部検索キーワード-->
      <v-col justify-start class="ml-3">
        <v-text-field
          label="外部DB検索keyword"
          :value="keyword"
          dense
          @input="(val) => (this.keyword = val)"
        />
      </v-col>
      <v-col class="pa-0 ma-0 mt-4">
        <v-btn class="ma-0 pa-0" elevation="1" fab x-small @click="flipKeyword">
          <v-icon>mdi-sync</v-icon>
        </v-btn>
      </v-col>
      <v-card outlined class="ml-2">
        <!--IMDB検索セレクタ-->
        <IDSelector
          label="imdb"
          site="imdb"
          :keyword="keyword"
          :id="event['outer_id'] ? event.outer_id['imdb'] : ''"
          @input="(id) => this.onIDChange('imdb', id)"
        />
        <!--映画DB検索セレクタ-->
        <IDSelector
          label="映画DB"
          site="eiga_db"
          :keyword="keyword"
          :id="event['outer_id'] ? event.outer_id['eiga_db'] : ''"
          @input="(id) => this.onIDChange('eiga_db', id)"
        />
      </v-card>
      <!--ローディング中オーバーレイ -->
      <v-overlay absolute :value="progress">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-row>
  </v-card>
</template>
<script>
import { ajaxGet } from "@/js/ajax.js";
export default {
  name: "OuterIDSelectPanel",
  props: ["event"],
  components: {
    IDSelector: () => import("./IDSelector"),
  },
  data() {
    return {
      retVal: {
        outer_id: { imdb: "", eiga_db: "" },
        img_src: { imdb: "", eiga_db: "" },
        outer_rate: { imdb: "", eiga_db: "" },
      },
      keyword: "",
      keywordFlip: true,
      progress: false,
    };
  },
  created() {
    this.setRetVal(
      "imdb",
      this.event["outer_id"] ? this.event["outer_id"]["imdb"] : "",
      this.event,
      true
    );
    this.setRetVal(
      "eiga_db",
      this.event["outer_id"] ? this.event["outer_id"]["eiga_db"] : "",
      this.event,
      true
    );
  },
  mounted() {
    this.keyword = this.event.title;
  },
  methods: {
    async onIDChange(site, id) {
      //ID受け取り後処理
      //サーバーに問い合わせて値を取得する
      this.progress = true;
      const response = await ajaxGet("/scrap/" + site + "/get/" + id);
      this.progress = false;
      this.setRetVal(site, id, response.data);
      this.$emit("input", this.retVal);
    },
    setRetVal(site, id, data, isEvent = false) {
      //リターン値をセットする
      //ID
      this.$set(this.retVal.outer_id, site, id);
      //英語タイトル
      if ("en_title" in data) {
        if (this.event["en_title"]) {
          //既存値を優先
          this.$set(this.retVal, "en_title", this.event["en_title"]);
        } else {
          this.$set(this.retVal, "en_title", data.en_title);
        }
        if (site == "imdb") {
          //IMDBのタイトル名を最優先
          this.$set(this.retVal, "en_title", data.en_title);
        }
      }
      //タイトル
      if ("title" in data && data.title.length > 0) {
        this.$set(this.retVal, "title", data.title);
      }
      //概要
      if ("outline" in data) {
        //既存値を優先
        if (
          !this.retVal["outline"] ||
          (this.retval["outline"] && this.retVal["outline"].length == 0)
        ) {
          this.$set(this.retVal, "outline", data.outline);
        }
      }
      //ポスターイメージ
      this.$set(
        this.retVal.img_src,
        site,
        "img_src" in data ? (isEvent ? data.img_src[site] : data.img_src) : ""
      );
      //レート
      this.$set(
        this.retVal.outer_rate,
        site,
        "rate" in data ? (isEvent ? data.rate[site] : data.rate) : ""
      );
    },
    flipKeyword() {
      //検索キーワード（タイトル/英語タイトル）切り替え
      var title = this.keywordFlip
        ? this.event["title"]
        : this.event["en_title"];
      if (String(title).length > 0) {
        this.keyword = title;
      }
      this.keywordFlip = !this.keywordFlip;
    },
  },
};
</script>