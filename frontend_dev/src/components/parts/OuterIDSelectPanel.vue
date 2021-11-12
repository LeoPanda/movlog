<template>
  <!--映画データベース検索コンポーネント-->
  <v-card width="100%" class="mx-1">
    <v-row>
      <!--外部検索キーワード-->
      <v-col justify-start class="ml-1">
        <v-text-field
          label="外部DB検索keyword"
          :value="keyword"
          dense
          @input="(val) => (this.keyword = val)"
        />
      </v-col>
      <v-col class="pa-0 ma-0 pt-3">
        <v-btn class="ma-0 pa-0" elevation="1" fab x-small @click="flipKeyword">
          <v-icon>mdi-sync</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <!--TMDB検索セレクタ-->
      <IDSelector
        label="TMDB"
        site="tmdb"
        :keyword="keyword"
        :id="event['outer_id'] ? event.outer_id['tmdb'] : ''"
        @input="(selected) => this.onIDChange('tmdb', selected.id)"
      />
    </v-row>
    <v-row>
      <!--IMDB検索セレクタ-->
      <IDSelector
        label="imdb"
        site="imdb"
        :keyword="keyword"
        :id="event['outer_id'] ? event.outer_id['imdb'] : ''"
        @input="(selected) => this.onIDChange('imdb', selected.id)"
      />
    </v-row>
    <v-row>
      <!--映画DB検索セレクタ-->
      <IDSelector
        label="映画DB"
        site="eiga_db"
        :keyword="keyword"
        :id="event['outer_id'] ? event.outer_id['eiga_db'] : ''"
        @input="(selected) => this.onIDChange('eiga_db', selected.id)"
      />
    </v-row>
    <!--ローディング中オーバーレイ -->
    <v-overlay absolute :value="progress">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-card>
</template>
<script>
import { ajaxGet } from "@/js/ajax.js";
import { getImgUrl } from "@/js/imgSizeControl";
export default {
  name: "OuterIDSelectPanel",
  props: ["event"],
  components: {
    IDSelector: () => import("./IDSelector"),
  },
  data() {
    return {
      keyword: "",
      keywordFlip: true,
      progress: false,
    };
  },
  mounted() {
    this.keyword = this.event.title;
  },
  methods: {
    getImgUrl,
    async onIDChange(site, id) {
      //ID受け取り後処理
      //サーバーに問い合わせて値を取得する
      this.progress = true;
      const response = await ajaxGet("/scrap/" + site + "/get/" + id);
      this.progress = false;
      this.setRetVal(site, id, response.data);
      this.$emit("input", this.event);
    },
    set_outer_key(key) {
      //外部サイトデータの初期化
      if (!(key in this.event)) {
        this.$set(this.event, key, { imdb: "", eiga_db: "", tmdb: "" });
      }
    },
    setRetVal(site, id, data) {
      //リターン値をセットする
      //ID
      this.set_outer_key("outer_id");
      this.$set(this.event.outer_id, site, id.toString());

      //英語タイトル
      if ("en_title" in data) {
        if (data.en_title.length > 0) {
          if (!("en_title" in this.event) || !this.event.en_title.length > 0) {
            this.$set(this.event, "en_title", data.en_title);
          }
        }
      }
      //タイトル
      if ("title" in data) {
        if (data.title.length > 0) {
          if (!("title" in this.event) || !this.event.title.length > 0) {
            this.$set(this.event, "title", data.title);
          }
        }
      }
      //概要
      if ("outline" in data) {
        if (data.outline.length > 0) {
          if (!("outline" in this.event) || !this.event.outline.length > 0) {
            this.$set(this.event, "outline", data.outline);
          }
        }
      }
      //ポスターイメージ
      this.set_outer_key("img_src");
      let img_src = "";
      if ("img_src" in data) {
        img_src = this.getImgUrl(data.img_src, "middle");
      }
      this.$set(this.event.img_src, site, img_src);
      //レート
      this.set_outer_key("outer_rate");
      let rate = "";
      if ("rate" in data) {
        rate = data.rate;
      }
      this.$set(this.event.outer_rate, site, rate);
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