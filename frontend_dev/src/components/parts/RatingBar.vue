<template>
  <!-- IMDB，映画DB上での評価レーティングを表示する -->
  <v-col align-self="end" float class="ml-2 ma-0 pa-0">
    <v-card-actions class="mt-0 pa-0">
      <!-- myレーティング -->
      <div class="d-flex text-caption" @click.stop="openRate(true)">
        <v-rating
          class="mx-0"
          :value="getRate"
          background-color="gray"
          color="yellow accent-4"
          half-increments
          length="5"
          dense
          readonly
          :size="getStarSize"
        />
        <div v-if="isDetail">({{ event["my_rate"] }})</div>
      </div>
      <!--myレート入力オーバーレイ-->
      <v-overlay :value="isOverlayed" absolute>
        <v-card class="d-flex">
          <v-rating
            class="d-flex"
            :value="event['my_rate']"
            color="yellow accent-4"
            @input="rateChanged"
            length="10"
            dense
          />
          <v-btn
            fab
            class="ma-1"
            color="blue-grey darken-1"
            x-small
            @click.stop="openRate(false)"
          >
            {{ event["my_rate"] }}</v-btn
          >
        </v-card>
      </v-overlay>
      <!-- IMDBリンクボタン -->
      <v-btn
        v-if="event.outer_id && event.outer_id.imdb"
        :x-small="!isDetail"
        color="accent"
        :class="isDetail ? 'mx-0 ml-1' : 'mx-0'"
        dense
        :width="getNumWidth"
        text
        @click="openWin('imdb', 'https://www.imdb.com/title/tt')"
        >IMDb<br />{{ imdbRate }}
      </v-btn>
      <!-- TMDBリンクボタン -->
      <v-btn
        v-if="event.outer_id && event.outer_id.tmdb"
        :x-small="!isDetail"
        class="mx-0"
        color="accent"
        dense
        :width="getNumWidth"
        text
        @click="openWin('tmdb', 'https://www.themoviedb.org/movie/')"
        >TMDB<br />{{ tmdbRate }}
      </v-btn>
      <!--googleカレンダーリンクボタン-->
      <v-btn
        class="mx-0"
        v-if="event.html_link && isDetail"
        color="accent"
        icon
        @click="openWin('calendar', event.html_link)"
        ><v-icon>mdi-calendar-clock</v-icon>
      </v-btn>
    </v-card-actions>
  </v-col>
</template>


<script>
import { setUploadItem } from "@/js/uploadControl";
import { ITEMS } from "@/js/serverDataItems";

export default {
  name: "RatingBar",
  props: ["event", "isNum"],
  data() {
    return { isOverlayed: false, isDetail: false };
  },
  mounted() {
    if (this.$route.path.match("/pages")) {
      this.isDetail = true;
    }
  },
  computed: {
    getRate() {
      //マイレート表示
      if ("my_rate" in this.event) {
        return Number(this.event.my_rate) / 2;
      } else {
        return 0;
      }
    },
    imdbRate() {
      //IMDBレート表示
      if (!this.isNum) {
        return "";
      }
      if ("outer_rate" in this.event && "imdb" in this.event.outer_rate) {
        return "(" + this.event.outer_rate.imdb + ")";
      } else {
        return "";
      }
    },
    getNumWidth() {
      return (this.isNum ? 60 : 30) + (this.isDetail ? 20 : 0);
    },
    tmdbRate() {
      //tmDBレート表示
      if (!this.isNum) {
        return "";
      }
      if ("outer_rate" in this.event && "tmdb" in this.event.outer_rate) {
        return "(" + this.event.outer_rate.tmdb + ")";
      } else {
        return "";
      }
    },
    getStarSize() {
      //レートスターの大きさ
      if (this.isDetail) {
        return 20;
      } else {
        return 16;
      }
    },
  },
  methods: {
    isVisible(item) {
      if (item in this.event > 0) {
        return true;
      } else {
        false;
      }
    },
    openRate(value) {
      //レート入力オーバレイを開く
      this.isOverlayed = value;
      this.$emit("openRate", this.isOverlayed);
    },
    rateChanged(value) {
      //レート変更時の処理
      this.$set(this.event, "my_rate", value);
      setUploadItem(ITEMS.events);
    },

    getLink(item, prefix) {
      //google calendarへのリンク表示
      if (this.event.outer_id && this.event.outer_id[item]) {
        return prefix + this.event.outer_id[item];
      } else {
        return prefix;
      }
    },
    openWin(item, prefix) {
      //別ウィンドウでリンク先を表示
      window.open(this.getLink(item, prefix), "_blank");
    },
  },
};
</script>